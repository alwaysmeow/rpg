import heapq
from typing import Dict

from core.command import Command

class CommandRecord:
    def __init__(self, time, command: Command, seq = 0):
        self.time = time
        self.command = command
        self.seq = seq

    def __lt__(self, other):
        if self.time == other.time:
            if self.command.priority == other.command.priority:
                return self.seq < other.seq
            return self.command.priority > other.command.priority
        return self.time < other.time

class CommandScheduler:
    def __init__(self, world, event_bus, game_config_path):
        self.world = world
        self.event_bus = event_bus
        self._queue = []
        self._unique_keys = set()
        self._seq: Dict[float, int] = {}

    def schedule(self, time, command: Command):
        unique_key = command.unique_key()
        if unique_key and unique_key in self._unique_keys:
            return None
        
        seq = self._seq.get(time, 0)
        self._seq[time] = seq + 1

        record = CommandRecord(time, command, seq)
        heapq.heappush(self._queue, record)

        if unique_key:
            self._unique_keys.add(unique_key)

        return record
    
    def process_one(self, now):
        if self.has_ready(now):
            record: CommandRecord = heapq.heappop(self._queue)
            unique_key = record.command.unique_key()
            self._unique_keys.discard(unique_key)

            event = record.command.execute(self.world)
            self.event_bus.queue(event)

    def has_ready(self, now):
        return bool(self._queue) and self._queue[0].time <= now

    def clear_seq_dict(self, now):
        keys_to_delete = [t for t in self._seq if t <= now]
        for t in keys_to_delete:
            del self._seq[t]