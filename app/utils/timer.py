import time


class Timer:
    """Timer class to measure time of execution of code"""
    
    def __init__(self):
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start
        print(f"Time taken: {round(self.elapsed, 4)} seconds")


if __name__ == '__main__':
    with Timer() as t:
        time.sleep(1)
