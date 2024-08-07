from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from concurrent.futures import Executor
import logging

class CustomExecutor(Executor):
    """CustomExecutor class to execute tasks using ThreadPoolExecutor or ProcessPoolExecutor."""

    def __init__(self, max_workers: int = None, executor_type: str = 'thread'):
        self.logger = logging.getLogger(__name__)
        self.max_workers = max_workers
        self.executor_type = executor_type
        self.executor = self.initialize_executor()
        self.logger.info(f'{self.executor_type} executor initialized')

    def initialize_executor(self):
        """Initialize executor based on type."""
        if self.executor_type == 'thread':
            return ThreadPoolExecutor(max_workers=self.max_workers)
        elif self.executor_type == 'process':
            return ProcessPoolExecutor(max_workers=self.max_workers)
        else:
            self.logger.error('Invalid executor type, using ThreadPoolExecutor')
            return ThreadPoolExecutor(max_workers=self.max_workers)

    def submit(self, fn, *args, **kwargs):
        return self.executor.submit(fn, *args, **kwargs)

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        return self.executor.map(fn, *iterables, timeout=timeout, chunksize=chunksize)

    def shutdown(self, wait=True):
        self.executor.shutdown(wait=wait)
        self.logger.info(f'{self.executor_type} executor shutdown')

    def __repr__(self):
        return f'{self.executor_type} executor'

    def __str__(self):
        return f'{self.executor_type} executor'
