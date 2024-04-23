"""Prep 8 Synthesize

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
Your task in this prep is to implement each of the unimplemented Tree methods
in this file.
The starter code has a recursive template that includes the "size-one" case;
you may or may not choose to use this in your final implementations.
"""
from __future__ import annotations

from typing import Any, Optional


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[Any]
    # The list of all subtrees of this tree.
    _subtrees: list[Tree]

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #   This setting of attributes represents an empty Tree.
    #
    #   Note: self._subtrees may be empty when self._root is not None.
    #   This setting of attributes represents a tree consisting of just one
    #   node.

    def __init__(self, root: Any, subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return True if this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also do len(subtree) here
            return size

    def num_positives(self) -> int:
        """Return the number of positive integers in this tree.

        Precondition: all items in this tree are integers.

        Remember, 0 is *not* positive.

        >>> t1 = Tree(17, [])
        >>> t1.num_positives()
        1
        >>> t2 = Tree(-10, [])
        >>> t2.num_positives()
        0
        >>> t3 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t3.num_positives()
        2
        """
        if self.is_empty():
            return 0
        elif self._subtrees == []:
            return 1 if self._root > 0 else 0
        else:
            counter = 1 if self._root > 0 else 0
            for subtree in self._subtrees:
                counter += subtree.num_positives()
            return counter

    def maximum(self: Tree) -> int:
        """Return the maximum item stored in this tree.

        Return 0 if this tree is empty.

        Precondition: all values in this tree are positive integers.

        >>> t1 = Tree(17, [])
        >>> t1.maximum()
        17
        >>> t3 = Tree(1, [Tree(12, []), Tree(10, []), Tree(30, [])])
        >>> t3.maximum()
        30
        """
        if self.is_empty():
            return -1
        elif self._subtrees == []:
            return self._root
        else:
            root_max = self._root
            for subtree in self._subtrees:
                root_max = max(root_max, subtree.maximum())
            return root_max

    def height(self: Tree) -> int:
        """Return the height of this tree.

        Please refer to the prep readings for the definition of tree height.

        >>> t1 = Tree(17, [])
        >>> t1.height()
        1
        >>> t2 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t2.height()
        2
        >>> t3 = Tree(1, [Tree(-2, [Tree(10, [Tree(-50, []), Tree(-40, []), Tree(-30, [])])])])
        >>> t3.height()
        4
        >>> t4 = Tree(1, [Tree(-2, [Tree(10, [Tree(-30, [Tree(-40, [])])])])])
        >>> t4.height()
        5
        """
        if self.is_empty():
            return 0
        elif self._subtrees == []:
            return 1
        else:
            max_sub_height = 0
            for subtree in self._subtrees:
                max_sub_height = max(max_sub_height, subtree.height())
            return max_sub_height + 1

    def __contains__(self, item: Any) -> bool:
        """Return whether this tree contains <item>.

        >>> t = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t.__contains__(-30)  # Could also write -30 in t.
        True
        >>> t.__contains__(148)
        False
        >>> t2 = Tree(1, [Tree(-2, [Tree(10, [Tree(-40, []), Tree(-30, [])])])])
        >>> t2.__contains__(-30)
        True
        >>> t2.__contains__(-40)
        True
        >>> t2.__contains__(10)
        True
        >>> t2.__contains__(114514)
        False
        """
        if self.is_empty():
            return False
        elif self._subtrees == []:
            return item == self._root
        else:
            if item == self._root:
                return True
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all()
