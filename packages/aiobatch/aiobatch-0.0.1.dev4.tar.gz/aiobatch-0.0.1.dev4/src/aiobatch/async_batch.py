import asyncio
import functools
import time

import numpy as np
import torch

from .batcher import TensorBatcher


class AsyncTask(object):
    def __init__(self, args: list, kwargs: dict) -> None:
        self.args = args
        self.kwargs = kwargs
        self._result = None
        self._done = asyncio.Event()

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

    async def get_result(self):
        await self._done.wait()
        return self._result


class AsyncBatchScheduler(object):
    def __init__(self, batch_size, timeout) -> None:
        self._queue = asyncio.Queue()
        self._worker = None
        self._stopped = False
        self._timeout = timeout
        self._batch_size = batch_size
        self._batcher = TensorBatcher(fixed_batch_size=batch_size)

    async def start(self, executor):
        if self._worker is not None:
            return
        self._executor = executor
        self._worker = asyncio.create_task(self._scheduler())
        self._stopped = False

    async def submit(self, task):
        await self._queue.put(task)

    async def _scheduler(self):
        last_task = None
        while not self._stopped:
            # Start a new batch
            if last_task is not None:
                task = last_task
                last_task = None
            else:
                task = await self._queue.get()
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
                    task = await asyncio.wait_for(self._queue.get(), timeout=wait)

                    if total_size + task.tensor_sample_num <= self._batch_size:
                        tasks.append(task)
                        total_size += task.tensor_sample_num
                    else:
                        last_task = task
                        break

                except asyncio.TimeoutError:
                    break

            if self._stopped:
                break

            args, kwargs = self._batcher.batch(tasks)
            # Process the batch
            # TODO(yuheng): pass stop event to executor
            result = await asyncio.to_thread(self._executor, *args, **kwargs)
            self._batcher.unbatch(tasks, result)

            tasks.clear()

    def stop(self):
        if self._worker is None:
            return
        self._stopped = True
        self._worker.cancel()
        self._worker = None
        self._executor = None

    def __call__(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            await self.start(func)

            task = AsyncTask(args, kwargs)
            await self.submit(task)

            return await task.get_result()

        return wrapper


class AsyncSingleScheduler(object):
    def __init__(self) -> None:
        self._queue = asyncio.Queue()
        self._worker = None
        self._stopped = False

    async def start(self, executor):
        if self._worker is not None:
            return
        self._executor = executor
        self._worker = asyncio.create_task(self._scheduler())
        self._stopped = False

    async def submit(self, task):
        await self._queue.put(task)

    async def _scheduler(self):
        while not self._stopped:
            args, kwargs, future = await self._queue.get()

            if self._stopped:
                break

            # TODO(yuheng): pass stop event to executor
            result = await asyncio.to_thread(self._executor, *args, **kwargs)
            future.set_result(result)

    def stop(self):
        if self._worker is None:
            return
        self._stopped = True
        self._worker.cancel()
        self._worker = None
        self._executor = None

    def __call__(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            await self.start(func)

            future = asyncio.Future()
            await self.submit((args, kwargs, future))

            return await future

        return wrapper


def async_queuing(batch_size=1, timeout=0):
    if batch_size == 1:
        return AsyncSingleScheduler()
    else:
        return AsyncBatchScheduler(batch_size, timeout)
