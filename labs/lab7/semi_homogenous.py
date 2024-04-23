from typing import Union


def semi_homogenous(obj: Union[int,list]) -> bool:
    """
    >>> semi_homogenous([[1], [2], [[3, 2, [4]]]])
    False
    >>> semi_homogenous([1, 2, [3]])
    False
    >>> semi_homogenous([[1], [2], [[3]]])
    True
    >>> semi_homogenous([[1], [2], [3]])
    True
    >>> semi_homogenous([1, 2, 3])
    True
    >>> semi_homogenous([[], [], []])
    True
    """
    if isinstance(obj, int):
        return True
    check_all = [semi_homogenous(sub) for sub in obj]
    for item in obj:
        if not isinstance(item, type(obj[0])):
            return False
    return all(check_all)