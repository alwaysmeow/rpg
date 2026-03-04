from dataclasses import dataclass, field
from engine.core.event import BaseEvent
from typing import List, Dict, Any

@dataclass
class BaseSnapshot:
    time: float = 0.0
    events: List[BaseEvent] = field(default_factory=list)
    entities: Dict[Any, Any] = field(default_factory=dict)