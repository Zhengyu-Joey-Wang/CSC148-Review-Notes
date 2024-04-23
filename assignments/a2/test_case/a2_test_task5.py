from tm_trees import TMTree


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


if __name__ == "__main__":
    import pytest

    pytest.main(["a2_test_task5.py"])
