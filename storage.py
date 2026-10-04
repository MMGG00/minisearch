import json

VERSION = 2


def save_state(filename, files):
    with open(filename, "w") as f:
        json.dump({"version": VERSION, "files": files}, f)


def load_state(filename):
    """Return the saved per-file records, or {} if there is no usable index yet."""
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    if data.get("version") != VERSION:
        return {}   # index from an older format: ignore it and rebuild
    return data["files"]