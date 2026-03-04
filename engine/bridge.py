from threading import Lock
from typing import Generic, TypeVar

from engine.core.snapshot import BaseSnapshot

S = TypeVar("S", bound=BaseSnapshot)

class Bridge(Generic[S]):
    def __init__(self):
        self._snapshot: S | None = None
        self._lock = Lock()

    def push_snapshot(self, snapshot: S):
        with self._lock:
            self._snapshot = snapshot

    def latest_snapshot(self) -> S | None:
        with self._lock:
            return self._snapshot