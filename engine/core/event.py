from dataclasses import dataclass

@dataclass
class BaseEvent: pass

@dataclass
class NoneEvent(BaseEvent): pass