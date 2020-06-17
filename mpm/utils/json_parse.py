from typing import List


def multiget(d: dict, keys: List[str], default=None):
    """
    Вытаскивает из словоря key из keys, если его нет, то пытается со следующим. 
    Если ничего не найденно то позвращает default
    """
    for key in keys:
        val = d.get(key, default)
        if val != default:
            return val
    return default
