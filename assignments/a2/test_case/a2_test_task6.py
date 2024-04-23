from papers import PaperTree


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


if __name__ == "__main__":
    import pytest

    pytest.main(["a2_test_task6.py"])
