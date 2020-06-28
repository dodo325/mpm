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

def iterative_topological_sort(graph: dict, start: "key", reverse=False, with_self=True) -> list:
    """
    >>> graph = {
        'a': ['b', 'c'],
        'b': ['d'],
        'c': ['d'],
        'd': ['e'],
        'e': []
    }
    >>> iterative_topological_sort(graph, 'a', reverse=True, with_self=False)
    ['e', 'd', 'c', 'b']
    >>> iterative_topological_sort(graph, 'a', reverse=True)
    ['e', 'd', 'c', 'b', 'a']
    >>> iterative_topological_sort(graph, 'a')
    ['a', 'b', 'c', 'd', 'e']
    >>> iterative_topological_sort(graph, 'e')
    ['e']
    >>> iterative_topological_sort(graph, 'c')
    ['c', 'd', 'e']
    """
    seen = set()
    stack = []    # path variable is gone, stack and order are new
    order = []    # order will be in reverse order at first
    q = [start]
    while q:
        v = q.pop()
        if v not in seen:
            seen.add(v)  # no need to append to path any more
            q.extend(graph[v])
            while stack and v not in graph[stack[-1]]:  # new stuff here!
                order.append(stack.pop())
            stack.append(v)
    out = stack + order[::-1]
    if reverse:
        out.reverse()
    if not with_self:
        out.remove(start)
    return out
