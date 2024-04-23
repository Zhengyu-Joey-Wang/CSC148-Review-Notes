"""CSC148 Lab 11: More on sorting

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module description ===
This file contains a mutating implementation of mergesort,
and a skeleton implementation of Timsort that you will work through
during this lab.
"""

from typing import Optional


###############################################################################
# Introduction: mutating version of mergesort
###############################################################################
def mergesort2(lst: list, start: int = 0, end: Optional[int] = None) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.

    Note: this is a *mutating, in-place* version of mergesort,
    meaning it does not return a new list, but instead sorts the input list.

    When we divide the list into halves, we don't create new lists for each
    half; instead, we simulate this by passing additional parameters (start
    and end) to represent the part of the list we're currently recursing on.
    """
    if end is None:
        end = len(lst)

    if start < end - 1:
        mid = (start + end) // 2
        mergesort2(lst, start, mid)
        mergesort2(lst, mid, end)
        _merge(lst, start, mid, end)


def _merge(lst: list, start: int, mid: int, end: int) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.

    Precondition: lst[start:mid] and lst[mid:end] are sorted.
    """
    result = []
    left = start
    right = mid
    while left < mid and right < end:
        if lst[left] < lst[right]:
            result.append(lst[left])
            left += 1
        else:
            result.append(lst[right])
            right += 1

    # This replaces lst[start:end] with the correct sorted version.
    lst[start:end] = result + lst[left:mid] + lst[right:end]


###############################################################################
# Task 1: Finding runs
###############################################################################
def find_runs(lst: list) -> list[tuple[int, int]]:
    """Return a list of tuples indexing the runs of lst.

    Precondition: lst is non-empty.

    >>> find_runs([1, 4, 7, 10, 2, 5, 3, -1])
    [(0, 4), (4, 6), (6, 7), (7, 8)]
    >>> find_runs([0, 1, 2, 3, 4, 5])
    [(0, 6)]
    >>> find_runs([10, 4, -2, 1])
    [(0, 1), (1, 2), (2, 4)]
    """
    runs = []

    # Keep track of the start and end points of a run.
    run_start = 0
    run_end = 1
    while run_end < len(lst):
        # How can you tell if a run should continue?
        #   (When you do, update run_end.)

        # How can you tell if a run is over?
        #   (When you do, update runs, run_start, and run_end.)
        if lst[run_end] < lst[run_end - 1]:
            runs.append((run_start, run_end))
            run_start = run_end
        run_end += 1
    runs.append((run_start, run_end))
    return runs


###############################################################################
# Task 2: Merging runs
###############################################################################
def timsort(lst: list) -> None:
    """Sort <lst> in place.

    >>> lst = []
    >>> timsort(lst)
    >>> lst
    []
    >>> lst = [1]
    >>> timsort(lst)
    >>> lst
    [1]
    >>> lst = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> timsort(lst)
    >>> lst
    [-1, 1, 2, 3, 4, 5, 7, 10]
    """
    runs = find_runs(lst)

    # Treat runs as a stack and repeatedly merge the top two runs
    # When the loop ends, the only run should be the whole list.
    # HINT: you should be able to use the "_merge" function provided
    # in this file.

    while len(runs) > 1:
        sub1 = runs.pop(0)
        sub2 = runs.pop(0)
        start = min(sub1[0], sub2[0])
        end = max(sub1[1], sub2[1])
        mid = max(sub1[0], sub2[0])
        _merge(lst, start, mid, end)
        runs.append((start, end))


# ###############################################################################
# # Task 3: Descending runs
# ###############################################################################
def find_runs2(lst: list) -> list[tuple[int, int]]:
    """Return a list of tuples indexing the runs of lst.

    Now, a run can be either ascending or descending!

    Precondition: lst is non-empty.

    First set of doctests, just for finding descending runs.
    # >>> find_runs2([5, 4, 3, 2, 1])
    # [(0, 5)]
    # >>> find_runs2([1, 4, 7, 10, 2, 5, 3, -1])
    # [(0, 4), (4, 6), (6, 8)]
    # >>> find_runs2([0, 1, 2, 3, 4, 5])
    # [(0, 6)]
    # >>> find_runs2([10, 4, -2, 1])
    # [(0, 3), (3, 4)]

    # The second set of doctests, to check that descending runs are reversed.
    # >>> lst1 = [5, 4, 3, 2, 1]
    # >>> find_runs2(lst1)
    # [(0, 5)]
    # >>> lst1  # The entire run is reversed
    # [1, 2, 3, 4, 5]
    >>> lst2 = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> find_runs2(lst2)
    [(0, 4), (4, 6), (6, 8)]
    >>> lst2  # The -1 and 3 are switched
    [1, 4, 7, 10, 2, 5, -1, 3]
    """
    # Hint: this is very similar to find_runs, except
    # you'll need to keep track of whether the "current run"
    # is ascending or descending.
    runs = []

    start = 0
    end = 1

    check_d = False
    while end < len(lst):
        if end-start == 1:
            check_d = True if lst[end] < lst[start] else False
            end += 1
            continue

        if check_d and lst[end] > lst[end - 1]:
            runs.append((start, end))
            lst[start:end] = lst[start:end][::-1]
            start = end
            check_d = False
        elif not check_d and lst[end] < lst[end - 1]:
            runs.append((start, end))
            start = end
        end += 1
    runs.append((start, end))
    if check_d:
        # print(start, end)
        lst[start:end] = lst[start:end][::-1]
    return runs


# ###############################################################################
# # Task 4: Minimum run length
# ###############################################################################
MIN_RUN = 64


def find_runs3(lst: list) -> list[tuple[int, int]]:
    """Same as find_runs2, but each run (except the last one)
    must be of length >= MIN_RUN.

    Precondition: lst is non-empty
    """
    runs = []

    start = 0
    end = 1

    check_d = False
    while end < len(lst):
        if start - end == 1:
            check_d = True if lst[end] < lst[start] else False
            end += 1
            continue

        if check_d and lst[end] > lst[end - 1]:
            lst[start:end] = lst[start:end][::-1]
            if end - start < 64:
                insertion_sort(lst, end, start + 64)
                end = start + 64
            runs.append((start, end))
            start = end
        elif not check_d and lst[end] < lst[end - 1]:
            runs.append((start, end))
            start = end
        end += 1
    runs.append(start, end)
    if check_d:
        lst[start:end] = lst[start:end][::-1]
    return runs


def insertion_sort(lst: list, start: int, end: int) -> None:
    """Sort the items in lst[start:end] in non-decreasing order."""
    for i in range(start + 1, end):
        num = lst[i]
        left = start
        right = i
        while right - left > 1:
            mid = (left + right) // 2
            if num < lst[mid]:
                right = mid
            else:
                left = mid + 1

        # insert
        if lst[left] > num:
            lst[left + 1 : i + 1] = lst[left:i]
            lst[left] = num
        else:
            lst[right + 1 : i + 1] = lst[right:i]
            lst[right] = num


###############################################################################
# Task 5: Optimizing merge
###############################################################################
def _merge2(lst: list, start: int, mid: int, end: int) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.

    Precondition: lst[start:mid] and lst[mid:end] are sorted.
    """
    sub = lst[start:mid]
    i = 0
    j = mid
    k = start
    while i < mid - start and j < end:
        if sub[i] <= lst[j]:
            lst[k] = sub[i]
            i += 1
        else:
            lst[k] = sub[j]
            j += 1
        k += 1

    lst[k:end] = sub[i:] + lst[j:end]


def timsort2(lst: list) -> None:
    """Sort <lst> in place.

    >>> lst = []
    >>> timsort(lst)
    >>> lst
    []
    >>> lst = [1]
    >>> timsort(lst)
    >>> lst
    [1]
    >>> lst = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> timsort(lst)
    >>> lst
    [-1, 1, 2, 3, 4, 5, 7, 10]
    """
    runs = find_runs2(lst)

    # Treat runs as a stack and repeatedly merge the top two runs
    # When the loop ends, the only run should be the whole list.
    # HINT: you should be able to use the "_merge" function provided
    # in this file.

    while len(runs) > 1:
        sub1 = runs.pop(0)
        sub2 = runs.pop(0)
        start = min(sub1[0], sub2[0])
        end = max(sub1[1], sub2[1])
        mid = max(sub1[0], sub2[0])
        _merge2(lst, start, mid, end)
        runs.append((start, end))


def timsort3(lst: list) -> None:
    """Sort <lst> in place.

    >>> lst = []
    >>> timsort(lst)
    >>> lst
    []
    >>> lst = [1]
    >>> timsort(lst)
    >>> lst
    [1]
    >>> lst = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> timsort(lst)
    >>> lst
    [-1, 1, 2, 3, 4, 5, 7, 10]
    """
    runs = find_runs3(lst)

    # Treat runs as a stack and repeatedly merge the top two runs
    # When the loop ends, the only run should be the whole list.
    # HINT: you should be able to use the "_merge" function provided
    # in this file.

    while len(runs) > 1:
        sub1 = runs.pop(0)
        sub2 = runs.pop(0)
        start = min(sub1[0], sub2[0])
        end = max(sub1[1], sub2[1])
        mid = max(sub1[0], sub2[0])
        _merge2(lst, start, mid, end)
        runs.append((start, end))


###############################################################################
# Task 6: Limiting the 'runs' stack
###############################################################################
def timsort2(lst: list) -> None:
    """Sort the given list using the version of timsort from Task 6."""
    pass
