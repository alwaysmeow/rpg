import heapq
from typing import Dict

from core.command import Command

from utils import load_config

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

        self.iterations = 0

        config = load_config(game_config_path)
        self.commands_per_tick_limit = config["commands_per_tick_limit"]

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

            self.iterations += 1

    def has_ready(self, now):
        return bool(self._queue) and self._queue[0].time <= now and self.iterations < self.commands_per_tick_limit

    def start_process(self):
        self.iterations = 0

    def end_process(self, now):
        # Delete sequence counters if all events processed
        if self.iterations < self.commands_per_tick_limit:
            self._clear_seq_dict(now)

    def _clear_seq_dict(self, now):
        keys_to_delete = [t for t in self._seq if t <= now]
        for t in keys_to_delete:
            del self._seq[t]