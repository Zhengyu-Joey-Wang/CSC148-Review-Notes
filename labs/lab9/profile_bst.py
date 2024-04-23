"""Lab 9: Binary Search Trees

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains some code for running some timing experiments on
binary search trees.
"""
import random
import sys
from timeit import timeit

from bst import BinarySearchTree


# ------------------------------------------------------------------------
# Task 3
# ------------------------------------------------------------------------
# TODO: implement this function!
def insert_delete_all(n: int, sorted_: bool) -> None:
    """Insert <n> items into an empty BinarySearchTree, and then remove them.

    If <sorted_> is True, the items should be inserted in sorted order.
    Otherwise, the items should be in *random* order.
    Hint: lookup how to use random.shuffle for this function.

    Precondition: n >= 0.

    Note: you'll need to first create your own BinarySearchTree here,
    and then call insert and delete on it.
    """
    pass


# This is the main timing experiment. You don't need to change any of the code
# below, although you can if you want to modify the experiment or plot the
# results using matplotlib.
if __name__ == '__main__':
    # Limit the depth of recursion to a level greater than is needed
    # for this lab exercise.  This will prevent incorrect code that has
    # infinite recursion from crashing Python. We'll discuss this more in
    # lecture.
    sys.setrecursionlimit(2000)

    SIZES = [100, 200, 400, 800, 1600]

    # For each of a series of list sizes, time insertion and deletion
    # into a bst from a RANDOMLY ORDERED list of that size.
    for size in SIZES:
        time = timeit('insert_delete_all(size, False)',
                      number=10, globals=globals())
        print(f'Random list of size {size:>7}, time {round(time, 6)}')

    # For each of a series of list sizes, time insertion and deletion
    # into a bst from a SORTED list of that size.
    for size in SIZES:
        time = timeit('insert_delete_all(size, True)',
                      number=10, globals=globals())
        print(f'Sorted list of size {size:>7}, time {round(time, 6)}')
