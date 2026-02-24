class TimeSystem:
    def __init__(self):
        self.now = 0.0

    def advance(self, delta):
        self.now += delta
        return self.now