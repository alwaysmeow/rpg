from dataclasses import dataclass, field

@dataclass
class BaseEvent:
    time: float = field(default=0.0, kw_only=True)

@dataclass
class NoneEvent(BaseEvent): pass