from tm_trees import TMTree


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


if __name__ == "__main__":
    import pytest

    pytest.main(["a2_test_get_tree_at_pos.py"])
