import os
import pytest
from tm_trees import TMTree, FileSystemTree

EXAMPLE_PATH = os.path.join(os.getcwd(), "example-directory", "workshop")


def test_file_system_init_t1() -> None:
    f = FileSystemTree(EXAMPLE_PATH)

    assert f._name == "workshop"
    assert f.data_size == 151
    assert len(f._subtrees) == 3
    f._subtrees.sort(key=lambda t: t._name)
    assert f._subtrees[0]._name == "activities"
    assert f._subtrees[1]._name == "draft.pptx"
    assert f._subtrees[2]._name == "prep"


if __name__ == "__main__":
    import pytest

    pytest.main(["my_a2_test.py"])
