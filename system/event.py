import heapq
from entity.event import Event

class EventSystem:
    def __init__(self):
        self._queue = []

    def schedule(self, time, handler):
        heapq.heappush(self._queue, Event(time, handler))

    def process(self, now):
        while self._queue and self._queue[0].time <= now:
            event = heapq.heappop(self._queue)
            event.handler()