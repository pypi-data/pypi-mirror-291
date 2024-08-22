"""Implements a thread pool executor."""

__author__ = "vex1023 (libao@vxquant.com)"
import os
import time
import logging

import itertools
import queue
import threading

from functools import wraps
from concurrent.futures import Future, BrokenExecutor, Executor
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Type,
    Set,
    Sequence,
    Iterable,
    Literal,
    Generic,
)
from vxutils.context import VXContext


class BrokenThreadPool(BrokenExecutor):
    pass


class VXFuture(Future[Any]):
    def __getattr__(self, __name: str) -> Any:
        return getattr(self.result(), __name)

    def __str__(self) -> str:
        try:
            return str(self.result(timeout=1))
        except TimeoutError:
            return super().__str__()

    def __repr__(self) -> str:
        try:
            return repr(self.result(timeout=1))
        except TimeoutError:
            return super().__repr__()

    __class__item__ = Generic


class VXTaskItem:
    def __init__(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.future: VXFuture[Any] = VXFuture()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, context: VXContext) -> None:
        if not self.future.set_running_or_notify_cancel():
            return

        try:
            result = self.handler_task(context=context)
            self.future.set_result(result)
        except BaseException as exc:
            self.future.set_exception(exc)

    def handler_task(self, context: VXContext) -> Any:
        return self.func(*self.args, **self.kwargs)


class VXBasicWorkerFactory(threading.Thread):
    """工作线程基类

    Arguments:
        work_queue {queue.Queue[VXTaskItem]} -- 任务队列
        idle_semaphore {threading.Semaphore} -- 信号量
        context {Optional[VXContext]} -- 上下文
        name {str} -- 线程名称
        idle_timeout {int} -- 空闲超时时间
    """

    def __init__(
        self,
        work_queue: queue.Queue[Optional[VXTaskItem]],
        idle_semaphore: threading.Semaphore,
        context: Optional[VXContext] = None,
        name: str = "",
        idle_timeout: Optional[int] = None,
    ) -> None:
        self._idle_semaphore = idle_semaphore
        self._idle_timeout = idle_timeout
        self._work_queue = work_queue
        self._context = context if context is not None else VXContext()
        return super().__init__(name=name, daemon=True, target=self.__worker_run__)

    @property
    def context(self) -> VXContext:
        """上下文"""
        return self._context

    def pre_run(self) -> None:
        logging.debug("worker %s start", self.name)

    def post_run(self) -> None:
        logging.debug("worker %s stop", self.name)

    def __worker_run__(self) -> None:
        try:
            self.pre_run()
        except BaseException as err:
            logging.error("worker pre_run error: %s", err, exc_info=True)
            raise BrokenThreadPool(err)

        try:
            while True:
                try:
                    task = self._work_queue.get_nowait()
                except queue.Empty:
                    self._idle_semaphore.release()
                    task = self._work_queue.get(timeout=self._idle_timeout)

                if task is None:
                    break

                task(self.context)
        except queue.Empty:
            pass

        finally:
            self._idle_semaphore.acquire(timeout=0)
            self.post_run()


def _result_or_cancel(fut: Future[Any], timeout: Optional[float] = None) -> Any:
    try:
        try:
            return fut.result(timeout)
        finally:
            fut.cancel()
    finally:
        # Break a reference cycle with the exception in self._exception
        del fut


class VXBasicPool:

    _counter = itertools.count().__next__

    def __init__(
        self,
        max_workers: Optional[int] = None,
        thread_name_prefix: str = "",
        worker_factory: Type[VXBasicWorkerFactory] = VXBasicWorkerFactory,
        context: Optional[VXContext] = None,
        idle_timeout: Optional[int] = 600,
    ) -> None:
        """Initializes a new VXExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            worker_factory: The factory class to create worker threads.
            context: The context to pass to worker threads.
            idle_timeout: The timeout in seconds to wait for a new task.

        """
        if max_workers is None:
            # VXExecutor is often used to:
            # * CPU bound task which releases GIL
            # * I/O bound task (which releases GIL, of course)
            #
            # We use cpu_count + 4 for both types of tasks.
            # But we limit it to 32 to avoid consuming surprisingly large resource
            # on many core machine.
            max_workers = min(32, (os.cpu_count() or 1) + 4)
        if max_workers <= 0:
            raise ValueError("max_workers must be greater than 0")

        self._max_workers = max_workers
        self._work_queue: queue.Queue[Optional[VXTaskItem]] = queue.Queue()
        self._idle_semaphore = threading.Semaphore(0)
        self._threads: Set[threading.Thread] = set()
        self._broken = False
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._thread_name_prefix = thread_name_prefix or self.__class__.__name__
        self._context = context
        self._worker_factory = worker_factory
        self._idle_timeout = idle_timeout

    def submit(self, task: VXTaskItem) -> VXFuture[Any]:
        """提交任务

        Arguments:
            task {VXTaskItem} -- 提交的任务

        Returns:
            Future[Any] -- 返回任务的 Future
        """

        with self._shutdown_lock:
            if self._broken:
                raise BrokenThreadPool(self._broken)

            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")

            self._work_queue.put(task)
            self._adjust_thread_count()
            return task.future

    def map(
        self, tasks: Sequence[VXTaskItem], *, timeout: Optional[float] = None
    ) -> Iterable[Any]:
        """批量提交任务

        Arguments:
            tasks {List[VXTaskItem]} -- 待提交的任务

        Raises:
            BrokenThreadPool: _description_
            RuntimeError: _description_

        Returns:
            Iterable[Any] -- 返回任务的 Future 列表
        """

        with self._shutdown_lock:
            if self._broken:
                raise BrokenThreadPool(self._broken)

            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")

            for task in tasks:
                self._work_queue.put(task)
                self._adjust_thread_count()

        def _result_iterator(
            fs: List[Future[Any]], timeout: Optional[float]
        ) -> Iterable[Any]:
            try:
                # reverse to keep finishing order
                fs.reverse()
                while fs:
                    # Careful not to keep a reference to the popped future
                    if timeout is None:
                        yield _result_or_cancel(fs.pop())
                    else:
                        yield _result_or_cancel(fs.pop(), timeout)
            finally:
                for future in fs:
                    future.cancel()

        return _result_iterator([task.future for task in tasks], timeout=timeout)

    def _adjust_thread_count(self) -> None:
        # if idle threads are available, don't spin new threads
        if self._idle_semaphore.acquire(timeout=0):
            return

        self._threads = {t for t in self._threads if t.is_alive()}
        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = f"{self._thread_name_prefix or self}_{VXBasicPool._counter()}"
            t = self._worker_factory(
                self._work_queue,
                self._idle_semaphore,
                self._context,
                name=thread_name,
                idle_timeout=self._idle_timeout,
            )
            t.start()
            self._threads.add(t)

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        with self._shutdown_lock:
            self._shutdown = True
            if cancel_futures:
                # Drain all work items from the queue, and then cancel their
                # associated futures.
                while not self._work_queue.empty():
                    try:
                        work_item = self._work_queue.get_nowait()
                    except queue.Empty:
                        break
                    if work_item is not None:
                        work_item.future.cancel()

            # Send a wake-up to prevent threads calling
            # _work_queue.get(block=True) from permanently blocking.
            for t in self._threads:
                self._work_queue.put(None)
        if wait:
            for t in self._threads:
                t.join()


class VXExecutor(Executor):
    """A thread pool executor.

    This class is a simple wrapper around the Python standard library's
    ThreadPoolExecutor class. It provides a more convenient way to create
    and manage thread pools.

    """

    def __init__(
        self,
        max_workers: Optional[int] = None,
        thread_name_prefix: str = "",
        *,
        idle_timeout: Optional[int] = None,
    ) -> None:
        """Initializes a new VXExecutor instance."""
        self._pool = VXBasicPool(
            max_workers, thread_name_prefix, idle_timeout=idle_timeout
        )
        super().__init__()

    def submit(
        self, fn: Callable[..., Any], /, *args: Any, **kwargs: Any
    ) -> VXFuture[Any]:
        """Submits a callable to be executed with the given arguments.

        Args:
            fn: The callable to execute.
            *args: The arguments to pass to the callable.
            **kwargs: The keyword arguments to pass to the callable.

        Returns:
            A Future representing the result of the callable.

        """
        task = VXTaskItem(fn, *args, **kwargs)
        return self._pool.submit(task)

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        self._pool.shutdown(wait, cancel_futures=cancel_futures)
        return super().shutdown(wait, cancel_futures=cancel_futures)


class async_task:
    """
    多线程提交任务
    example::

        @async_task
        def test():
            time.sleep(1)
    """

    __executor__ = VXExecutor(thread_name_prefix="async_task", idle_timeout=600)

    def __init__(
        self,
        max_workers: int = 5,
        on_error: Literal["logging", "raise", "ignore"] = "raise",
    ) -> None:
        self._semaphore = threading.Semaphore(max_workers)
        self._on_error = on_error

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:

        def semaphore_func(*args: Any, **kwargs: Any) -> Any:
            with self._semaphore:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    if self._on_error == "logging":
                        logging.error(
                            "async_task error: %s",
                            err,
                            exc_info=True,
                            stack_info=True,
                        )
                    elif self._on_error == "raise":
                        raise err from err

                    return None

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> VXFuture:
            return self.__executor__.submit(semaphore_func, *args, **kwargs)

        return wrapper


def async_map(
    func: Callable[..., Any],
    *iterables: Any,
    timeout: Optional[float] = None,
    chunsize: int = 1,
) -> Any:
    """异步map提交任务

    Arguments:
        func {Callable[..., Any]} -- 运行func

    Returns:
        Any -- 返回值
    """
    return async_task.__executor__.map(
        func, *iterables, timeout=timeout, chunksize=chunsize
    )


if __name__ == "__main__":
    start = time.perf_counter()
    pool = VXExecutor(5, "hello_world")

    @async_task(on_error="ignore")
    def test(i: int) -> int:
        logging.warning(f"task {i} start")
        time.sleep(0.1 * i)
        raise ValueError(f"task {i} error")
        # return f"{i + 1} done"

    print([test(i) for i in range(5)])
    print(time.perf_counter() - start)
