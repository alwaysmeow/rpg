class Health:
    def __init__(self, base_max_value, base_regen):
        self.base_max_value = base_max_value
        self.base_regen = base_regen
        self.effective_max_value = base_max_value
        self.effective_regen = base_regen
        self.value = base_max_value
