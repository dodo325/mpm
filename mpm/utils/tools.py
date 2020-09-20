from typing import List

def inheritors(cls: "Class") -> List["Class"]:
    """Get all class inheritors

    Returns:
        List["class"]: return all subclasses
    """
    subclasses = []
    work = [cls]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.append(child)
                work.append(child)
    return subclasses
