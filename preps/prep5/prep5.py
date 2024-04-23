"""Prep 5 Synthesize

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.
"""
from __future__ import annotations

from typing import Any, Optional


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: Optional[_Node]

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # next initially points to nothing


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    _first: Optional[_Node]

    def __init__(self) -> None:
        """Initialize an empty linked list.
        """
        self._first = None

    def print_items(self) -> None:
        """Print out each item in this linked list."""
        curr = self._first
        while curr is not None:
            print(curr.item)
            curr = curr.next

    # ------------------------------------------------------------------------
    # Prep 5 exercises
    # ------------------------------------------------------------------------
    # For each of the following linked list methods, read its docstring
    # and then complete its implementation.
    # You should use our *linked list traversal* code template as your
    # starting point, but of course you should modify it as necessary!
    #
    # NOTE: the first two methods are new special methods (you can tell by the
    # double underscores), and enable some special Python behaviour that we've
    # illustrated in the doctests.
    #
    # At the bottom of this file, we've included some helpers
    # to create some basic linked lists for our doctests.
    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedList()
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = three_items(1, 2, 3)
        >>> len(lst)
        3
        """
        curr = self._first
        counter = 0
        while curr is not None:
            counter += 1
            curr = curr.next
        return counter

    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this list.

        Use == to compare items.

        >>> lst = three_items(1, 2, 3)
        >>> 2 in lst                     # Equivalent to lst.__contains__(2)
        True
        >>> 4 in lst
        False
        """
        curr = self._first
        while curr is not None:
            if curr.item == item:
                return True
            curr = curr.next
        return False

    # HINTS: for this one, you'll be adding a new item to a linked list.
    #   1. Create a new _Node object first.
    #   2. Consider the cases where the list is empty and non-empty separately.
    #   3. For the non-empty case, you'll first need to iterate to the
    #      *last node* in the linked list. (Review this prep's Quercus quiz!)
    def append(self, item: Any) -> None:
        """Append <item> to the end of this list.

        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst._first.item
        1
        >>> lst.append(2)
        >>> lst._first.next.item
        2
        """
        if self._first is None:
            self._first = _Node(item)
            return
        curr = self._first
        while curr.next is not None:
            curr = curr.next
        curr.next = _Node(item)

# ------------------------------------------------------------------------
# Helpers for creating linked lists (testing purposes only)
# ------------------------------------------------------------------------


def one_item(x: Any) -> LinkedList:
    """Return a linked list containing the given item."""
    lst = LinkedList()
    node = _Node(x)
    lst._first = node
    return lst


def three_items(x1: Any, x2: Any, x3: Any) -> LinkedList:
    """Return a linked list containing the given three items."""
    lst = LinkedList()
    node1 = _Node(x1)
    node2 = _Node(x2)
    node3 = _Node(x3)
    node1.next = node2
    node2.next = node3
    lst._first = node1
    return lst


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['print_items', 'LinkedList.print_items'],
        # This configuration setting ignores the problem with
        # one_item and three_items accessing a private attribute.
        'exclude-protected': ['_first']
    })

    # import doctest
    # doctest.testmod()
