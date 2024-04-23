"""Lab 6: Recursion

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains a few nested list functions for you to practice recursion.
"""
from typing import Union


def add_n(obj: Union[int, list], n: int) -> Union[int, list]:
    """Return a new nested list where <n> is added to every item in <obj>.

    >>> add_n(10, 3)
    13
    >>> add_n([1, 2, [1, 2], 4], 10)
    [11, 12, [11, 12], 14]
    """
    if isinstance(obj, int):
        return obj + n
    for i in range(len(obj)):
        obj[i] = add_n(obj[i], n)
    return obj
        


def nested_list_equal(obj1: Union[int, list], obj2: Union[int, list]) -> bool:
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.

    >>> nested_list_equal(17, [1, 2, 3])
    False
    >>> nested_list_equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> nested_list_equal([1, 2, [1, 2], 4], [4, 2, [2, 1], 3])
    False
    """
    if isinstance(obj1, int) and isinstance(obj2, int):
        return obj1 == obj2
    elif not isinstance(obj1, type(obj2)) or len(obj1) != len(obj2):
        return False
    for i in range(len(obj1)):
        if not nested_list_equal(obj1[i], obj2[i]):
            return False
    return True
        


def duplicate(obj: Union[int, list]) -> Union[int, list]:
    """Return a new nested list with all numbers in <obj> duplicated.

    Each integer in <obj> should appear twice *consecutively* in the
    output nested list. The nesting structure is the same as the input,
    only with some new numbers added. See doctest examples for details.

    If <obj> is an int, return a list containing two copies of it.

    >>> duplicate(1)
    [1, 1]
    >>> duplicate([])
    []
    >>> duplicate([1, 2])
    [1, 1, 2, 2]
    >>> duplicate([1, [2, 3]])  # NOT [1, 1, [2, 2, 3, 3], [2, 2, 3, 3]]
    [1, 1, [2, 2, 3, 3]]
    """
    if isinstance(obj, int):
        return [obj, obj]
    idx = 0
    while idx < len(obj):
        dup = duplicate(obj[idx])
        if isinstance(obj[idx], int):
            obj.insert(idx, dup[0])
            idx += 1
        else:
            obj[idx] = dup
        idx += 1
    return obj


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all()
