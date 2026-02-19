import time

class Clock:
    def __init__(self):
        self._last = time.perf_counter()

    def get_delta(self):
        now = time.perf_counter()
        delta = now - self._last
        self._last = now
        return delta
