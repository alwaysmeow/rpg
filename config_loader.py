import json

def load_config(path: str):
    with open(path, "r") as f:
        return json.load(f)