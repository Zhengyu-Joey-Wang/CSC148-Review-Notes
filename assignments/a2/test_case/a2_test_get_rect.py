from tm_trees import TMTree


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


if __name__ == "__main__":
    import pytest

    pytest.main(["a2_test_get_rect.py"])
