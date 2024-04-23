import os
from tm_trees import TMTree, FileSystemTree


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


########################
# edge case start here #
########################
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


if __name__ == "__main__":
    import pytest

    pytest.main(["a2_test_update_rect.py"])
