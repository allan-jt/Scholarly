import time
from contextlib import contextmanager, asynccontextmanager

@contextmanager
def log(message: str):
    start_time = time.time()
    print(f'{message}...')
    yield
    print(f'{message} completed in {time.time() - start_time:.2f} seconds.')

@asynccontextmanager
async def log_async(message: str):
    start_time = time.time()
    print(f'{message}...')
    yield
    print(f'{message} completed in {time.time() - start_time:.2f} seconds.')
