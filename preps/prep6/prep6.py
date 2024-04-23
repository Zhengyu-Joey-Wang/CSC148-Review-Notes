"""Prep 6 Synthesize

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
Your task in this prep is to implement each of the following recursive functions
on nested lists, using the following steps for *Recursive Function Design*:

1.  Identify the recursive structure of the input (in this case, always a nested
    list), and write down the code template for nested lists:

    def f(obj: Union[int, list]) -> ...:
        if isinstance(obj, int):
            ...
        else:
            ...
            for sublist in obj:
                ... f(sublist) ...
            ...

2.  Implement the base case(s) directly (in this case, a single integer).
3.  Write down a concrete example with a somewhat complex argument, (in this
    case, a nested list with around 3 sub-nested-lists), and then write down
    the relevant recursive calls and what they should return.
4.  Determine how to combine the recursive calls to compute the correct output.
    Make sure you can express this in English first, and then implement your
    idea.

HINT: The implementations here should be similar to ones you've seen
before in the readings or comprehension questions.
"""
from typing import Union


def num_positives(obj: Union[int, list]) -> int:
    """Return the number of positive integers in <obj>.

    Remember, 0 is *not* positive.

    >>> num_positives(17)
    1
    >>> num_positives(-10)
    0
    >>> num_positives([1, -2, [-10, 2, [3], 4, -5], 4])
    5
    """
    if isinstance(obj, int):
        return 1 if obj > 0 else 0
    counter = 0
    for sub in obj:
        counter += num_positives(sub)
    return counter


def nested_max(obj: Union[int, list]) -> int:
    """Return the maximum integer stored in nested list <obj>.

    Return 0 if <obj> is an empty list.

    Precondition: all integers in <obj> are positive.

    >>> nested_max(17)
    17
    >>> nested_max([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    if isinstance(obj, int):
        return obj
    ans = 0
    for i in obj:
        ans = max(ans, nested_max(i))
    return ans


def max_length(obj: Union[int, list]) -> int:
    """Return the maximum length of any list in nested list <obj>.

    The *maximum length* of a nested list is defined as:
    1. 0, if <obj> is a number.
    2. The maximum of len(obj) and the lengths of the nested lists contained
       in <obj>, if <obj> is a list.

    >>> max_length(17)
    0
    >>> max_length([1, 2, [1, 2], 4])
    4
    >>> max_length([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    if isinstance(obj, int):
        return 0
    max_len = len(obj)
    for sub in obj:
        max_len = max(max_len, max_length(sub))
    return max_len


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all()
