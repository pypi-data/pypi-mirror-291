import functools
import queue
import threading
import time
from concurrent.futures import Future

import numpy as np
import torch

from .batcher import TensorBatcher


class Task(object):
    def __init__(self, args: list, kwargs: dict) -> None:
        self.args = args
        self.kwargs = kwargs
        self._result = None
        self._done = threading.Event()

        self._prepare()

    def _prepare(self):
        args_idx = []
        kwargs_idx = []
        tensor_sample_num = None
        for i, arg in enumerate(self.args):
            if isinstance(arg, torch.Tensor) or isinstance(arg, np.ndarray):
                args_idx.append(i)
                if tensor_sample_num is None:
                    tensor_sample_num = arg.shape[0]
                elif tensor_sample_num != arg.shape[0]:
                    raise ValueError(
                        "All tensor arguments should have the same batch size"
                    )

        for key, value in self.kwargs.items():
            if isinstance(value, torch.Tensor) or isinstance(value, np.ndarray):
                kwargs_idx.append(key)
                if tensor_sample_num is None:
                    tensor_sample_num = value.shape[0]
                elif tensor_sample_num != value.shape[0]:
                    raise ValueError(
                        "All tensor arguments should have the same batch size"
                    )

        self.tensor_args_idx = args_idx
        self.tensor_kwargs_idx = kwargs_idx
        self.tensor_sample_num = tensor_sample_num
        if tensor_sample_num is None:
            raise ValueError("No tensor arguments found")

    def set_result(self, result):
        self._result = result
        self._done.set()

    def get_result(self):
        self._done.wait()
        return self._result


class BatchScheduler(object):
    def __init__(self, batch_size, timeout) -> None:
        self._queue = queue.Queue()
        self._worker_thread = None
        self._stop_event = threading.Event()
        self._timeout = timeout
        self._batch_size = batch_size
        self._batcher = TensorBatcher(fixed_batch_size=batch_size)

    def start(self, executor):
        if self._worker_thread is not None:
            return
        self._executor = executor
        self._worker_thread = threading.Thread(target=self._scheduler, daemon=True)
        self._worker_thread.start()

    def submit(self, task):
        self._queue.put(task)

    def _scheduler(self):
        last_task = None
        while not self._stop_event.is_set():
            # Start a new batch
            if last_task is not None:
                task = last_task
                last_task = None
            else:
                task = self._queue.get()
            tasks = [task]
            total_size = task.tensor_sample_num

            since = time.time()
            # Add more tasks to the batch, until the batch is full or timeout
            while (
                self._timeout > 0
                and total_size < self._batch_size
                and not self._stop_event.is_set()
            ):
                try:
                    elapsed = time.time() - since
                    wait = self._timeout - elapsed
                    if wait < 0:
                        break
                    task = self._queue.get(timeout=wait)

                    if total_size + task.tensor_sample_num <= self._batch_size:
                        tasks.append(task)
                        total_size += task.tensor_sample_num
                    else:
                        last_task = task
                        break

                except queue.Empty:
                    break

            if self._stop_event.is_set():
                break

            args, kwargs = self._batcher.batch(tasks)
            # Process the batch
            # TODO(yuheng): pass stop event to executor
            result = self._executor(*args, **kwargs)
            self._batcher.unbatch(tasks, result)

            tasks.clear()

    def stop(self):
        if self._worker_thread is None:
            return
        self._stop_event.set()
        self._worker_thread.join()
        self._worker_thread = None
        self._executor = None

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.start(func)

            task = Task(args, kwargs)
            self.submit(task)

            return task.get_result()

        return wrapper


class SingleScheduler(object):
    def __init__(self) -> None:
        self._queue = queue.Queue()
        self._worker_thread = None
        self._stop_event = threading.Event()

    def start(self, executor):
        if self._worker_thread is not None:
            return
        self._executor = executor
        self._worker_thread = threading.Thread(target=self._scheduler, daemon=True)
        self._worker_thread.start()

    def submit(self, task):
        self._queue.put(task)

    def _scheduler(self):
        while not self._stop_event.is_set():
            args, kwargs, future = self._queue.get()
            if self._stop_event.is_set():
                break

            # TODO(yuheng): pass stop event to executor
            result = self._executor(*args, **kwargs)
            future.set_result(result)

    def stop(self):
        if self._worker_thread is None:
            return
        self._stop_event.set()
        self._worker_thread.join()
        self._worker_thread = None
        self._executor = None

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.start(func)

            future = Future()
            self.submit((args, kwargs, future))
            return future.result()

        return wrapper


def queuing(batch_size=1, timeout=0):
    if batch_size == 1:
        return SingleScheduler()
    else:
        return BatchScheduler(batch_size, timeout)
