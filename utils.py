import json

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def load_config(path: str):
    with open(path, "r") as f:
        return json.load(f)