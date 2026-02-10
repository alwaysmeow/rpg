class Event:
    def __init__(self, time, handler):
        self.time = time
        self.handler = handler

    def __lt__(self, other):
        return self.time < other.time