"""
Assignment 2 - Sample Tests

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains sample tests for Assignment 2, Tasks 1 and 2.
The tests use the provided example-directory, so make sure you have downloaded
and extracted it into the same place as this test file.
This test suite is very small. You should plan to add to it significantly to
thoroughly test your code.

IMPORTANT NOTES:
    - If using PyCharm, go into your Settings window, and go to
      Editor -> General.
      Make sure the "Ensure line feed at file end on Save" is NOT checked.
      Then, make sure none of the example files have a blank line at the end.
      (If they do, the data size will be off.)

    - os.listdir behaves differently on different
      operating systems.  These tests expect the outcomes that one gets
      when running on the *Teaching Lab machines*.
      Please run all of your tests there - otherwise,
      you might get inaccurate test failures!

    - Depending on your operating system or other system settings, you
      may end up with other files in your example-directory that will cause
      inaccurate test failures. That will not happen on the Teachin Lab
      machines.  This is a second reason why you should run this test module
      there.
"""

import os

from hypothesis import given
from hypothesis.strategies import integers

from tm_trees import TMTree, FileSystemTree
from papers import PaperTree

# This should be the path to the "workshop" folder in the sample data.
# You may need to modify this, depending on where you downloaded and
# extracted the files.
EXAMPLE_PATH = os.path.join(os.getcwd(), "example-directory", "workshop")


def test_single_file() -> None:
    """Test a tree with a single file."""
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, "draft.pptx"))
    assert tree._name == "draft.pptx"
    assert tree._subtrees == []
    assert tree._parent_tree is None
    assert tree.data_size == 58
    assert is_valid_colour(tree._colour)


def test_example_data() -> None:
    """Test the root of the tree at the 'workshop' folder in the example data"""
    tree = FileSystemTree(EXAMPLE_PATH)
    assert tree._name == "workshop"
    assert tree._parent_tree is None
    assert tree.data_size == 151
    assert is_valid_colour(tree._colour)

    assert len(tree._subtrees) == 3
    for subtree in tree._subtrees:
        # Note the use of is rather than ==.
        # This checks ids rather than values.
        assert subtree._parent_tree is tree


@given(
    integers(min_value=100, max_value=1000),
    integers(min_value=100, max_value=1000),
    integers(min_value=100, max_value=1000),
    integers(min_value=100, max_value=1000),
)
def test_single_file_rectangles(x, y, width, height) -> None:
    """Test that the correct rectangle is produced for a single file."""
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, "draft.pptx"))
    tree.update_rectangles((x, y, width, height))
    rects = tree.get_rectangles()

    # This should be just a single rectangle and colour returned.
    assert len(rects) == 1
    rect, colour = rects[0]
    assert rect == (x, y, width, height)
    assert is_valid_colour(colour)


def test_example_data_rectangles() -> None:
    """This test sorts the subtrees, because different operating systems have
    different behaviours with os.listdir.

    You should *NOT* do any sorting in your own code
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    tree.update_rectangles((0, 0, 200, 100))
    tree.expand_all()
    rects = tree.get_rectangles()

    # IMPORTANT: This test should pass when you have completed Task 2, but
    # will fail once you have completed Task 5.
    # You should edit it as you make progress through the tasks,
    # and add further tests for the later task functionality.
    assert len(rects) == 6

    # UPDATED:
    # Here, we illustrate the correct order of the returned rectangles.
    # Note that this corresponds to the folder contents always being
    # sorted in alphabetical order. This is enforced in these sample tests
    # only so that you can run them on your own computer, rather than on
    # the Teaching Labs.
    actual_rects = [r[0] for r in rects]
    expected_rects = [
        (0, 0, 94, 2),
        (0, 2, 94, 28),
        (0, 30, 94, 70),
        (94, 0, 76, 100),
        (170, 0, 30, 72),
        (170, 72, 30, 28),
    ]

    assert len(actual_rects) == len(expected_rects)
    for i in range(len(actual_rects)):
        assert expected_rects[i] == actual_rects[i]


###########################
# My test case start here #
###########################


def test_file_system_init_t1() -> None:
    f = FileSystemTree(EXAMPLE_PATH)

    assert f._name == "workshop"
    assert f.data_size == 151
    assert len(f._subtrees) == 3
    f._subtrees.sort(key=lambda t: t._name)
    assert f._subtrees[0]._name == "activities"
    assert f._subtrees[1]._name == "draft.pptx"
    assert f._subtrees[2]._name == "prep"


def test_size_zero_t2ur() -> None:
    subt = [TMTree("st1", []), TMTree("st2", [])]
    tree = TMTree("t1", subt)
    tree.update_rectangles((0, 0, 200, 200))

    assert tree.rect == (0, 0, 0, 0)
    assert tree._subtrees[0].rect == tree._subtrees[1].rect == (0, 0, 0, 0)


def test_single_leaf_node_t2ur() -> None:
    tree = TMTree("t", [], 100)

    assert tree.data_size == 100

    tree.update_rectangles((0, 0, 100, 100))
    assert tree.rect == (0, 0, 100, 100)


def test_equal_size_t2ur() -> None:
    subtrees = [TMTree(f"st{i}", [], 50) for i in range(4)]
    tree = TMTree("t", subtrees)

    assert tree.data_size == 200

    tree.update_rectangles((0, 0, 200, 100))
    e_ract = [(0, 0, 50, 100), (50, 0, 50, 100), (100, 0, 50, 100), (150, 0, 50, 100)]
    for i in range(4):
        assert subtrees[i].rect == e_ract[i]


def test_diff_size_t2ur() -> None:
    subtrees = [TMTree("st1", [], 15), TMTree("st2", [], 38)]
    tree = TMTree("t", subtrees)
    assert tree.data_size == 53
    tree.update_rectangles((0, 0, 100, 100))

    assert subtrees[0].rect == (0, 0, 100, 28)
    assert subtrees[1].rect == (0, 28, 100, 72)


def test_nested_trees_t2ur() -> None:
    sstree = TMTree("sstree", [], 100)
    stree = TMTree("stree", [sstree], 100)
    tree = TMTree("tree", [stree], 100)
    tree.update_rectangles((0, 0, 300, 300))

    assert tree.rect == (0, 0, 300, 300)
    assert stree.rect == (0, 0, 300, 300)
    assert sstree.rect == (0, 0, 300, 300)


def test_one_empty_foder_t2ur() -> None:
    st1 = TMTree("st1", [], 1)
    st2 = TMTree("st2", [], 2)
    ef1 = TMTree("ef1", [])
    t = TMTree("t", [st1, st2, ef1])

    assert t.data_size == 3

    t.update_rectangles((0, 0, 50, 100))
    assert st1.rect == (0, 0, 50, 33)
    assert st2.rect == (0, 33, 50, 66)
    assert ef1.rect == (0, 0, 0, 0)


def test_empty_tree_t2gr() -> None:
    tree = TMTree("root", [])
    assert tree.data_size == 0
    assert not tree.get_rectangles()

    tree = TMTree(None, [])
    assert not tree._subtrees
    assert tree.data_size == 0
    tree.update_rectangles((0, 0, 10, 10))
    tree.expand_all()
    assert len(tree.get_rectangles()) == 0


def test_single_node_tree_t2gr() -> None:
    tree = TMTree("root", [], 100)
    tree.update_rectangles((0, 0, 50, 50))
    assert tree.get_rectangles()[0][0] == (0, 0, 50, 50)


def test_tree_with_zero_sized_subtrees_t2gr() -> None:
    subtrees = [TMTree(f"st{i}", [], 0) for i in range(3)]
    tree = TMTree("root", subtrees)
    assert tree.data_size == 0
    tree.update_rectangles((0, 0, 100, 100))
    assert not tree.get_rectangles()


def test_nested_single_path_t2gr() -> None:
    leaf = TMTree("leaf", [], 1)
    inter = TMTree("inter", [leaf])
    root = TMTree("root", [inter])
    assert leaf.data_size == inter.data_size == root.data_size == 1
    root.update_rectangles((0, 0, 100, 100))
    assert root.get_rectangles()[0][0] == (0, 0, 100, 100)


def test_large_number_subtrees_t2gr() -> None:
    subtrees = [TMTree(f"leaf{i}", [], 1) for i in range(1000)]
    tree = TMTree("root", subtrees)
    assert tree.data_size == 1000
    tree.expand_all()
    tree.update_rectangles((0, 0, 1000, 1000))
    assert len(tree.get_rectangles()) == 1000


def test_some_subtrees_collapse_t2gr() -> None:
    sub1 = TMTree("sub1", [TMTree("leaf", [], 51), TMTree("leaf", [], 1)])
    sub2 = TMTree("sub2", [TMTree("leaf", [], 50), TMTree("leaf", [], 2)])
    root = TMTree("root", [sub1, sub2])
    assert sub1.data_size == 52
    assert sub2.data_size == 52
    assert root.data_size == 104

    root.expand_all()
    sub1._subtrees[1].collapse()

    root.update_rectangles((0, 0, 100, 100))
    all_rect = [sub[0] for sub in root.get_rectangles()]
    assert len(all_rect) == 3

    assert sub1.rect in all_rect
    assert sub1._subtrees[0] not in all_rect
    assert sub1._subtrees[1] not in all_rect

    assert sub2._subtrees[0].rect in all_rect
    assert sub2._subtrees[1].rect in all_rect

    assert root.rect not in all_rect


def test_get_rect_have_zero_size_t2gr() -> None:
    st1 = TMTree("st1", [], 1)
    st2 = TMTree("st2", [], 2)
    ef1 = TMTree("ef1", [], 0)
    t = TMTree("t", [st1, st2, ef1])

    t.expand_all()
    t.update_rectangles((0, 0, 50, 100))

    assert st1.rect == (0, 0, 50, 33)
    assert st2.rect == (0, 33, 50, 66)
    assert ef1.rect == (0, 0, 0, 0)

    all_rect = [sub[0] for sub in t.get_rectangles()]
    assert len(all_rect) == 2
    assert st1.rect in all_rect
    assert st2.rect in all_rect
    assert ef1.rect not in all_rect


def test_pos_bound_working_t3gtap() -> None:
    f1 = TMTree("f1", [], 10)
    f2 = TMTree("f2", [], 10)
    root = TMTree("root", [f1, f2])
    assert root.data_size == 20
    root.update_rectangles((0, 0, 100, 100))

    # check unexpanded root
    assert root.get_tree_at_position((0, 0)) == root
    assert root.get_tree_at_position((0, 100)) == root
    assert root.get_tree_at_position((100, 0)) == root
    assert root.get_tree_at_position((100, 100)) == root
    assert root.get_tree_at_position((25, 48)) == root
    assert root.get_tree_at_position((150, 150)) is None
    assert root.get_tree_at_position((-1, 0)) is None
    assert root.get_tree_at_position((0, -1)) is None
    assert root.get_tree_at_position((0, 101)) is None
    root.expand_all()

    assert root.get_tree_at_position((0, 0)) == f1
    assert root.get_tree_at_position((0, 50)) == f1
    assert root.get_tree_at_position((100, 50)) == f1
    assert root.get_tree_at_position((0, 51)) == f2
    assert root.get_tree_at_position((100, 100)) == f2


def test_very_small_subtree_t3gtap() -> None:
    f = TMTree("f", [], 1)
    f.update_rectangles((0, 0, 1, 1))
    assert f.get_tree_at_position((0, 0)) == f
    assert f.get_tree_at_position((1, 1)) == f
    assert f.get_tree_at_position((1, 0)) == f
    assert f.get_tree_at_position((0, 1)) == f


def test_get_empty_size_t3gtap() -> None:
    st1 = TMTree("st1", [], 1)
    st2 = TMTree("st2", [], 2)
    ef1 = TMTree("ef1", [], 0)
    t = TMTree("t", [st1, st2, ef1])
    t.expand_all()
    t.update_rectangles((0, 0, 50, 100))
    assert st1.rect == (0, 0, 50, 33)
    assert st2.rect == (0, 33, 50, 66)
    assert ef1.rect == (0, 0, 0, 0)

    assert t.get_tree_at_position((0, 100)) is None


def test_get_none_empty_size_t3gtap() -> None:
    st1 = TMTree("st1", [], 1)
    st2 = TMTree("st2", [], 2)
    ef1 = TMTree("ef1", [], 0)
    f1 = TMTree("f1", [], 3)
    t1 = TMTree("t1", [st1, st2, ef1])
    t2 = TMTree("t2", [f1])
    root = TMTree("root", [t1, t2])

    root.expand_all()
    root.update_rectangles((0, 0, 50, 100))

    assert st1.rect == (0, 0, 50, 16)
    assert st2.rect == (0, 16, 50, 33)
    assert t2.rect == (0, 50, 50, 50)
    assert f1.rect == (0, 50, 50, 50)
    assert ef1.rect == (0, 0, 0, 0)

    assert root.get_tree_at_position((0, 10)) == st1
    assert root.get_tree_at_position((0, 0)) == st1
    assert root.get_tree_at_position((50, 16)) == st1
    assert root.get_tree_at_position((10, 17)) == st2
    assert root.get_tree_at_position((50, 17)) == st2
    assert root.get_tree_at_position((50, 49)) == st2
    assert root.get_tree_at_position((50, 100)) == f1
    assert root.get_tree_at_position((25, 63)) == f1
    assert root.get_tree_at_position((50, 50)) is None


######################
# test change_size() #
######################
def test_change_size_one_leaf_t4() -> None:
    leaf = TMTree("l1", [], 10)
    assert leaf._expanded == False
    leaf.change_size(0.1)
    assert leaf.data_size == 11
    leaf.change_size(-0.1)
    assert leaf.data_size == 9
    leaf.change_size(-10000)
    assert leaf.data_size == 1


def test_change_size_on_root_t4() -> None:
    st1 = TMTree("st1", [], 10)
    st2 = TMTree("st2", [], 10)
    root = TMTree("root", [st1, st2])
    assert root.data_size == 20
    root.change_size(0.1)
    assert root.data_size == 20
    assert st1.data_size == 10
    assert st2.data_size == 10


def test_change_size_with_root_t4() -> None:
    st1 = TMTree("st1", [], 10)
    st2 = TMTree("st2", [], 10)
    root = TMTree("root", [st1, st2])
    assert root.data_size == 20

    st1.change_size(0.1)
    assert st1.data_size == 11
    assert st2.data_size == 10
    assert root.data_size == 21

    st2.change_size(-0.00000001)
    assert st1.data_size == 11
    assert st2.data_size == 9
    assert root.data_size == 20


def test_change_size_below_zero_t4() -> None:
    st1 = TMTree("st1", [], 10)
    st2 = TMTree("st2", [], 10)
    root = TMTree("root", [st1, st2])
    assert root.data_size == 20

    st1.change_size(-10000)
    assert st1.data_size == 1
    assert st2.data_size == 10
    assert root.data_size == 11

    st2.change_size(-10000)
    assert st1.data_size == 1
    assert st2.data_size == 1
    assert root.data_size == 2


def test_nested_change_size1_t4() -> None:
    leaf1 = TMTree("l1", [], 10)
    st1 = TMTree("st1", [leaf1])
    st2 = TMTree("st2", [], 10)
    root = TMTree("root", [st1, st2])
    assert root.data_size == 20
    assert st1.data_size == 10

    leaf1.change_size(-0.1)
    assert leaf1.data_size == 9
    assert st1.data_size == 9
    assert root.data_size == 19


def test_nested_change_size2_t4() -> None:
    leaf1 = TMTree("l1", [], 10)
    st1 = TMTree("st1", [leaf1])
    st2 = TMTree("st2", [], 10)
    root = TMTree("root", [st1, st2])
    assert root.data_size == 20
    assert st1.data_size == 10

    leaf1.change_size(0.1)
    assert leaf1.data_size == 11
    assert st1.data_size == 11
    assert root.data_size == 21


############################
# test update_data_sizes() #
############################
def test_leaf_expand_update_size_t4() -> None:
    leaf1 = TMTree("l1", [], 10)
    leaf1._expanded = True
    size = leaf1.update_data_sizes()
    assert size == 10
    assert leaf1._expanded == True

    leaf2 = TMTree("l2", [], 10)
    root = TMTree("root", [leaf1, leaf2])
    size = root.update_data_sizes()
    assert size == 20


def test_update_size_one_leaf_t4() -> None:
    leaf = TMTree("leaf", [], 10)
    root = TMTree("root", [leaf])

    assert root.data_size == 10
    leaf.data_size = 50
    assert root.data_size == 10

    assert leaf.update_data_sizes() == 50
    assert root.data_size == 10
    assert root.update_data_sizes() == 50
    assert root.data_size == 50


def test_update_size_nested_tree_t4() -> None:
    leaf1 = TMTree("leaf", [], 10)
    leaf2 = TMTree("leaf", [], 10)
    leaf3 = TMTree("leaf", [], 10)
    st1 = TMTree("st1", [leaf1, leaf2])
    st2 = TMTree("st2", [leaf3])
    t = TMTree("t", [st1, st2])
    root = TMTree("root", [t])
    assert root.data_size == 30
    assert t.data_size == 30
    assert st1.data_size == 20
    assert st2.data_size == 10

    leaf2.data_size = 20

    assert st2.update_data_sizes() == 10
    assert st1.data_size == 20

    assert st2.update_data_sizes() == 10
    assert st1.data_size == 20
    assert st2.data_size == 10
    assert t.data_size == 30
    assert root.data_size == 30
    root.update_data_sizes()
    assert root.data_size == 40
    assert t.data_size == 40


###############
# test move() #
###############


# unseccess move
def test_move_folder_t4() -> None:
    st1 = TMTree("st1", [], 10)
    folder = TMTree("folder", [st1])
    st2 = TMTree("st2", [], 20)
    dst = TMTree("dst", [st2])
    root = TMTree("root", [folder, dst])
    assert root.data_size == 30

    folder.move(dst)
    assert folder.data_size == 10
    assert folder._parent_tree == root
    assert st1._parent_tree == folder
    assert len(folder._subtrees) == 1
    assert folder._subtrees[0] == st1
    assert dst.data_size == 20
    assert len(dst._subtrees) == 1
    assert dst._subtrees[0] == st2


def test_move_to_empty_folder_t4() -> None:
    st1 = TMTree("st1", [], 10)
    folder = TMTree("folder", [st1])
    dst = TMTree("dst", [])
    root = TMTree("root", [dst, folder])
    assert root.data_size == 10
    assert dst.data_size == 0

    st1.move(dst)
    assert dst.data_size == 0
    assert not dst._subtrees
    assert folder.data_size == 10
    assert len(folder._subtrees) == 1
    assert folder._subtrees[0] == st1
    assert folder._parent_tree == root
    assert st1._parent_tree == folder


# seccess move
def test_move_leaf_t4() -> None:
    leaf = TMTree("l1", [], 10)
    scr = TMTree("s", [leaf])
    node = TMTree("n1", [], 20)
    dst = TMTree("dst", [node])
    root = TMTree("root", [scr, dst])
    assert dst.data_size == 20
    assert scr.data_size == 10
    assert root.data_size == 30

    root.update_rectangles((0, 0, 100, 100))

    root.expand_all()

    leaf.move(dst)
    assert dst.data_size == 30
    assert len(dst._subtrees) == 2
    assert dst._subtrees[0] == node
    assert dst._subtrees[1] == leaf
    assert leaf._parent_tree == dst

    assert len(scr._subtrees) == 0
    assert scr._parent_tree == root
    assert not scr._subtrees
    assert scr.rect == (0, 0, 100, 33)
    assert scr.data_size == 0
    assert scr._expanded == False

    assert root.data_size == 30


def test_nested_leaf_move_t4() -> None:
    leaf = TMTree("l1", [], 10)
    st1 = TMTree("s", [leaf])
    scr = TMTree("scr", [st1])
    node = TMTree("n1", [], 20)
    dst = TMTree("dst", [node])
    root = TMTree("root", [scr, dst])
    assert root.data_size == 30

    root.expand_all()
    leaf.move(dst)

    assert leaf._parent_tree == dst
    assert not st1._subtrees
    assert st1.data_size == 0
    assert len(scr._subtrees) == 1
    assert st1 in scr._subtrees
    assert scr.data_size == 0

    assert len(dst._subtrees) == 2
    assert dst._subtrees[0] == node
    assert dst._subtrees[1] == leaf

    assert root.data_size == 30
    assert leaf._expanded == False
    assert st1._expanded == False
    assert scr._expanded == True
    assert node._expanded == False
    assert dst._expanded == True
    assert root._expanded == True


def test_move_leaf_in_mutileafs_t4() -> None:
    leaf = TMTree("l1", [], 10)
    leaf2 = TMTree("l2", [], 10)
    st1 = TMTree("s", [leaf, leaf2])
    scr = TMTree("scr", [st1])
    node = TMTree("n1", [], 20)
    dst = TMTree("dst", [node])
    root = TMTree("root", [scr, dst])
    assert root.data_size == 40
    assert scr.data_size == 20
    root.expand_all()
    leaf.move(dst)

    assert leaf._parent_tree == dst
    assert st1.data_size == 10
    assert len(st1._subtrees) == 1
    assert leaf not in st1._subtrees
    assert leaf2 in st1._subtrees
    assert len(scr._subtrees) == 1
    assert st1 in scr._subtrees
    assert scr.data_size == 10

    assert len(dst._subtrees) == 2
    assert dst._subtrees[0] == node
    assert dst._subtrees[1] == leaf

    assert root.data_size == 40
    assert leaf._expanded == False
    assert st1._expanded == True
    assert scr._expanded == True
    assert node._expanded == False
    assert dst._expanded == True
    assert root._expanded == True


######################
# test delete_self() #
######################
def test_delete_without_parent_t4() -> None:
    tree = TMTree("t", [], 10)
    assert tree.delete_self() == False


def test_delete_single_leaf_t4() -> None:
    leaf = TMTree("leaf", [], 10)
    root = TMTree("root", [leaf])
    assert root.data_size == 10

    assert root._expanded == False
    root.expand_all()
    assert root._expanded == True
    assert leaf._expanded == False

    assert leaf.delete_self() == True
    assert not root._subtrees
    assert root.data_size == 0
    assert root._expanded == False


def test_delete_nested_leaf_t4() -> None:
    target = TMTree("leaf", [], 10)
    subsub1 = TMTree("sst1", [target])
    sub1 = TMTree("st1", [subsub1])
    leaf1 = TMTree("l1", [], 5)
    root = TMTree("root", [sub1, leaf1])
    assert root.data_size == 15

    assert root._expanded == False
    root.update_rectangles((0, 0, 100, 100))
    root.expand_all()
    assert root._expanded == True
    assert subsub1._expanded == True
    assert target._expanded == False

    target.delete_self()
    assert not subsub1._subtrees
    assert subsub1.data_size == 0
    assert sub1.data_size == 0
    assert root.data_size == 5
    assert subsub1.rect == (0, 0, 100, 66)
    assert sub1.rect == (0, 0, 100, 66)
    assert root.get_tree_at_position((10, 10)) == subsub1

    assert root._expanded == True
    assert subsub1._expanded == False
    assert sub1._expanded == True

    # check affter value after call update_rect
    assert subsub1.data_size == 0
    root.update_rectangles((0, 0, 100, 100))
    assert subsub1.data_size == 0
    assert subsub1 in sub1._subtrees
    assert subsub1.rect == (0, 0, 0, 0)
    assert sub1.rect == (0, 0, 0, 0)


def test_delete_leaf_in_mutileafs_t4() -> None:
    target = TMTree("target", [], 10)
    leaf1 = TMTree("l1", [], 5)
    subsub1 = TMTree("sst1", [target, leaf1])
    sub1 = TMTree("st1", [subsub1])
    leaf2 = TMTree("leaf", [], 5)
    root = TMTree("root", [sub1, leaf2])
    assert sub1.data_size == 15
    assert root.data_size == 20

    assert root._expanded == False
    root.update_rectangles((0, 0, 100, 100))
    root.expand_all()
    assert root._expanded == True
    assert subsub1._expanded == True

    target.delete_self()
    assert subsub1.data_size == 5
    assert len(subsub1._subtrees) == 1
    assert target not in subsub1._subtrees
    assert leaf1 in subsub1._subtrees
    assert sub1.data_size == 5
    assert root.data_size == 10
    assert subsub1.rect == (0, 0, 100, 75)
    assert sub1.rect == (0, 0, 100, 75)
    assert leaf1.rect == (66, 0, 34, 75)

    assert root._expanded == True
    assert subsub1._expanded == True
    assert sub1._expanded == True


def test_expand_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    st1 = TMTree("st1", [leaf1])
    st2 = TMTree("st2", [leaf2])
    root = TMTree("root", [st1, st2])

    assert root._expanded == False
    root.expand()
    assert root._expanded == True
    assert st1._expanded == False
    assert st2._expanded == False
    st1.expand()
    assert st1._expanded == True
    assert st2._expanded == False
    assert leaf1._expanded == False
    assert leaf2._expanded == False
    st2.expand()
    assert st1._expanded == True
    assert st2._expanded == True
    assert leaf1._expanded == False
    assert leaf2._expanded == False
    leaf1.expand()
    assert leaf1._expanded == False
    assert leaf2._expanded == False
    leaf2.expand()
    assert leaf1._expanded == False
    assert leaf2._expanded == False


def test_root_expand_all_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand_all()
    assert leaf1._expanded == False
    assert leaf2._expanded == False
    assert sst1._expanded == True
    assert sst2._expanded == True
    assert st._expanded == True
    assert root._expanded == True


def test_subtree_expand_all1_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand()
    st.expand()
    sst1.expand_all()
    assert ssst1._expanded == False
    assert sst2._expanded == False
    assert sst1._expanded == True
    assert leaf1._expanded == leaf2._expanded == leaf3._expanded == False
    assert root._expanded == st._expanded == True


def test_subtree_expand_all2_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand()
    st.expand()
    sst2.expand_all()
    assert ssst1._expanded == True
    assert sst2._expanded == True
    assert sst1._expanded == False
    assert leaf1._expanded == leaf2._expanded == leaf3._expanded == False
    assert root._expanded == st._expanded == True


def test_collapse_one_leaf_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    st1 = TMTree("st1", [leaf1])
    root = TMTree("root", [st1])
    root.expand_all()
    leaf1._expanded == False
    leaf1.collapse()
    assert st1._expanded == False
    st1.collapse()
    assert root._expanded == False


def test_collapse_muti_leaf1_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand_all()
    leaf3.collapse()
    ssst1.collapse()
    sst1.collapse()
    assert root._expanded == True
    assert st._expanded == False
    assert sst1._expanded == False


def test_collapse_muti_leaf2_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand_all()
    leaf2.collapse()
    assert root._expanded == True
    assert leaf1._expanded == False
    assert leaf2._expanded == False
    assert leaf3._expanded == False
    assert ssst1._expanded == False
    assert sst2._expanded == False
    assert sst1._expanded == True
    assert st._expanded == True


def test_collapse_muti_leaf3_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand_all()
    leaf1.collapse()
    sst1.collapse()
    assert root._expanded == True
    assert leaf1._expanded == False
    assert leaf2._expanded == False
    assert leaf3._expanded == False
    assert ssst1._expanded == False
    assert sst2._expanded == False
    assert sst1._expanded == False
    assert st._expanded == False


def test_collapse_all_on_leaf1_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand_all()
    leaf1.collapse_all()

    check_list = [leaf1, leaf2, leaf3, ssst1, sst1, sst2, st, root]
    for check in check_list:
        assert check._expanded == False


def test_collapse_all_on_leaf2_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand_all()
    leaf2.collapse_all()

    check_list = [leaf1, leaf2, leaf3, ssst1, sst1, sst2, st, root]
    for check in check_list:
        assert check._expanded == False


def test_collapse_all_on_leaf3_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand_all()
    leaf3.collapse_all()

    check_list = [leaf1, leaf2, leaf3, ssst1, sst1, sst2, st, root]
    for check in check_list:
        assert check._expanded == False


def test_collapse_all_on_ssst1_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand_all()
    leaf3.collapse()
    ssst1.collapse_all()

    check_list = [leaf1, leaf2, leaf3, ssst1, sst1, sst2, st, root]
    for check in check_list:
        assert check._expanded == False


def test_collapse_all_on_sst_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand_all()
    leaf1.collapse()
    sst1.collapse_all()

    check_list = [leaf1, leaf2, leaf3, ssst1, sst1, sst2, st, root]
    for check in check_list:
        assert check._expanded == False


def test_collapse_all_on_st_t5() -> None:
    leaf1 = TMTree("file", [], 10)
    leaf2 = TMTree("file", [], 10)
    leaf3 = TMTree("file", [], 10)
    ssst1 = TMTree("ssst1", [leaf3])
    sst1 = TMTree("sst1", [leaf1])
    sst2 = TMTree("sst2", [leaf2, ssst1])
    st = TMTree("st", [sst1, sst2])
    root = TMTree("root", [st])

    root.expand_all()
    leaf1.collapse()
    sst1.collapse_all()
    st.collapse_all()

    check_list = [leaf1, leaf2, leaf3, ssst1, sst1, sst2, st, root]
    for check in check_list:
        assert check._expanded == False


def test_all_papers_t6() -> None:
    paper_tree = PaperTree("CS1", [], all_papers=False)
    assert not paper_tree._subtrees
    paper_tree = PaperTree("CS1", [], all_papers=False, by_year=True)
    assert not paper_tree._subtrees
    paper_tree = PaperTree("CS1", [], all_papers=False, by_year=False)
    assert not paper_tree._subtrees
    paper_tree = PaperTree("CS1", [], all_papers=True)
    assert paper_tree._subtrees


def test_by_year_t6() -> None:
    paper_tree = PaperTree("CS1", [], all_papers=True, by_year=True)
    for sub in paper_tree._subtrees:
        assert sub._name.isdigit()
    paper_tree = PaperTree("CS1", [], all_papers=True, by_year=False)
    for sub in paper_tree._subtrees:
        assert not sub._name.isdigit()


##############################################################################
# Helpers
##############################################################################


def is_valid_colour(colour: tuple[int, int, int]) -> bool:
    """Return True iff <colour> is a valid colour. That is, if all of its
    values are between 0 and 255, inclusive.
    """
    for i in range(3):
        if not 0 <= colour[i] <= 255:
            return False
    return True


def _sort_subtrees(tree: TMTree) -> None:
    """Sort the subtrees of <tree> in alphabetical order.
    THIS IS FOR THE PURPOSES OF THE SAMPLE TEST ONLY; YOU SHOULD NOT SORT
    YOUR SUBTREES IN THIS WAY. This allows the sample test to run on different
    operating systems.

    This is recursive, and affects all levels of the tree.
    """
    if not tree.is_empty():
        for subtree in tree._subtrees:
            _sort_subtrees(subtree)

        tree._subtrees.sort(key=lambda t: t._name)


if __name__ == "__main__":
    import pytest

    pytest.main(["a2_sample_test.py"])
