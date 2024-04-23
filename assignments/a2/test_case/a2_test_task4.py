from tm_trees import TMTree


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


if __name__ == "__main__":
    import pytest

    pytest.main(["a2_test_task4.py"])
