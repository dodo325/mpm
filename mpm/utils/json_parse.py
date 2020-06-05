from typing import List


def multiget(d: dict, keys: List[str], default):
    for key in keys:
        val = d.get(key, default)
        if val != default:
            return val
    return default


