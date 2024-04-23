"""
Assignment 2: Trees for Treemap

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton,
                   Haocheng Hu, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None

        self._expanded = False

        self._colour = self._gen_color()
        if self._name is None or not self._subtrees:
            self.data_size = data_size
            self._subtrees = []
            return
        sub_sum = 0
        for sub in self._subtrees:
            # cal total subtrees data_size
            sub_sum += sub.data_size
            # set parent tree for subtrees
            sub._parent_tree = self
        self.data_size = sub_sum

    def _gen_color(self) -> Tuple[int, int, int]:
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        if self.is_empty():
            return
        if self.data_size == 0:
            self._set_subtree_rect_to_zero()
            return
        if not self._subtrees:
            self.rect = rect
            return
        x, y, width, height = rect
        height_used, width_used = 0, 0
        for i in range(len(self._subtrees) - 1):
            subtree = self._subtrees[i]
            if subtree.is_empty():
                continue
            sub_size = subtree.data_size
            if height >= width:
                sub_height = int(sub_size / self.data_size * height)
                sub_rect = (x, y, width, sub_height)
                subtree.update_rectangles(sub_rect)
                y += sub_height
                height_used += sub_height
            else:
                sub_width = int(sub_size / self.data_size * width)
                sub_rect = (x, y, sub_width, height)
                subtree.update_rectangles(sub_rect)
                x += sub_width
                width_used += sub_width
        last_subtree = self._subtrees[-1]
        if height >= width:
            last_subtree.update_rectangles((x, y, width, height - height_used))
        else:
            last_subtree.update_rectangles((x, y, width - width_used, height))
        self.rect = rect

    def _set_subtree_rect_to_zero(self) -> None:
        if not self._subtrees:
            self.rect = (0, 0, 0, 0)
            return
        for sub in self._subtrees:
            sub._set_subtree_rect_to_zero()
        self.rect = (0, 0, 0, 0)

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.is_empty() or self.data_size == 0:
            return []
        if not self._subtrees or not self._expanded:
            return [(self.rect, self._colour)]
        return sum([sub.get_rectangles() for sub in self._subtrees], [])

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        if self.is_empty():
            return None
        if not self._subtrees or not self._expanded:
            return self if self._check_vild_pos(pos) else None
        for sub in self._subtrees:
            if sub._check_vild_pos(pos):
                subtree = sub.get_tree_at_position(pos)
                return subtree
        return None

    def _check_vild_pos(self, pos: Tuple[int, int]) -> bool:
        x, y, width, height = self.rect
        return x <= pos[0] <= x + width and y <= pos[1] <= y + height

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self.is_empty():
            return 0
        if not self._subtrees:
            return self.data_size
        sub_size = 0
        for sub in self._subtrees:
            sub_size += sub.update_data_sizes()
        self.data_size = sub_size
        return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if self.is_empty() or self._subtrees or self._parent_tree is None \
                or not destination._subtrees:
            return
        pt = self.get_parent()
        destination._subtrees.append(self)
        destination.data_size += self.data_size
        self._parent_tree = destination
        pt._subtrees.remove(self)
        if not pt._subtrees:
            pt._expanded = False
        dst_p = destination._parent_tree
        if dst_p is None:
            dst_p = destination
        pt._move_update_size(dst_p, self.data_size)

    def _move_update_size(self, dst_p: TMTree, size: int) -> None:
        if self._parent_tree is None or self == dst_p:
            return
        self.data_size -= size
        self._parent_tree._move_update_size(dst_p, size)

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if self.is_empty() or self._subtrees:
            return
        op_sign = 1 if factor >= 0 else -1
        size_change = math.ceil(self.data_size * abs(factor)) * op_sign
        if self.data_size + size_change < 1:
            size_change = -self.data_size + 1
        self.data_size += size_change
        if self._parent_tree is not None:
            self._parent_tree._add_on_panrent(size_change)

    def _add_on_panrent(self, size_change: int) -> None:
        if self._parent_tree is None:
            self.data_size += size_change
            return
        self.data_size += size_change
        self._parent_tree._add_on_panrent(size_change)

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful.

        Only do this if this node has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualiser to go back to the parent folder.
        """
        if self._parent_tree is None:
            return False
        removed_size = self.data_size

        parent_tree = self._parent_tree
        parent_tree._subtrees.remove(self)
        if not parent_tree._subtrees:
            parent_tree._expanded = False

        parent_tree.data_size -= self.data_size
        while parent_tree._parent_tree is not None:
            parent_tree = parent_tree._parent_tree
            parent_tree.data_size -= removed_size
        return True

    def expand(self) -> None:
        """ Expand the current tree if the subtree is not empty"""
        if self.is_empty() or not self._subtrees:
            return
        self._expanded = True

    def expand_all(self) -> None:
        """ Expand current tree and all subtree """
        if self.is_empty() or not self._subtrees:
            return
        for sub in self._subtrees:
            sub.expand_all()
        self._expanded = True

    def collapse(self) -> None:
        """ Unexpand/collapse the current tree to its parent tree
        if parent tree is None, then nothing happend
        """
        if self._parent_tree is None:
            return
        self._parent_tree._collapse_subtree()

    def _collapse_subtree(self) -> None:
        if self.is_empty() or not self._subtrees:
            self._expanded = False
        for sub in self._subtrees:
            sub._collapse_subtree()
        self._expanded = False

    def collapse_all(self) -> None:
        """ Unexpand/collapse all the tree.
        (A.K.A. back to the root node)
        """
        if self._parent_tree is None:
            self._unexpanded_all_subtrees()
            return
        self._parent_tree.collapse_all()

    def _unexpanded_all_subtrees(self) -> None:
        if self.is_empty() or self._subtrees == []:
            self._expanded = False
            return
        for sub in self._subtrees:
            sub._unexpanded_all_subtrees()
        self._expanded = False

    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        root_name = os.path.basename(path)
        if not os.path.isdir(path):
            size = os.path.getsize(path)
            super().__init__(root_name, [], size)
            return
        sub_files = os.listdir(path)
        sub_files_tree = [self._gen_subtree(path, fn) for fn in sub_files]
        super().__init__(root_name, sub_files_tree)

    def _gen_subtree(self, path: str, filename: str) -> FileSystemTree:
        return FileSystemTree(os.path.join(path, filename))

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
