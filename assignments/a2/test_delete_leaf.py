from tm_trees import TMTree

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


if __name__ == "__main__":
    import pytest

    pytest.main(["test_delete_leaf.py"])