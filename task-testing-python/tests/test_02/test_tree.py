import pytest
from tree_utils_02.node import FileNode
from tree_utils_02.tree import Tree


def test_construct(tmp_path):
    tree = Tree()
    path = tmp_path / "construct.txt"
    path.write_text("text")

    assert tree.construct_filenode(path, False) == FileNode(name="construct.txt", is_dir=False, children=[])

def test_update(tmp_path):
    tree = Tree()
    node = FileNode(name=tmp_path, is_dir=True, children=[])

    assert tree.update_filenode(node) == FileNode(name=tmp_path, is_dir=True, children=[])

def test_get_raises_if_path_not_exists(tmp_path):
    tree = Tree()
    missing_path = tmp_path / "not_exists"

    with pytest.raises(AttributeError) as exc_info:
        tree.get(missing_path, False)

    assert str(exc_info.value) == "Path not exist"

def test_get_file_with_no_dirsonly(tmp_path):
    tree = Tree()
    file_path = tmp_path / "a.txt"
    file_path.write_text("hello")

    assert tree.get(file_path, False) == FileNode(name="a.txt", is_dir=False, children=[])

def test_get_file_with_dirsonly_no_recursive(tmp_path):
    tree = Tree()
    file_path = tmp_path / "a.txt"
    file_path.write_text("hello")

    with pytest.raises(AttributeError) as exc_info:
        tree.get(file_path, True)

    assert str(exc_info.value) == "Path is not directory"

def test_get_file_with_dirsonly_recursive(tmp_path):
    tree = Tree()
    file_path = tmp_path / "a.txt"
    file_path.write_text("hello")

    assert tree.get(file_path, True, True) is None

def test_get_dir_with_children(tmp_path):
    tree = Tree()
    first_dir = tmp_path / "first_dir"
    first_dir.mkdir()
    (first_dir / "a.txt").write_text("first_file")
    (first_dir / "b.txt").write_text("second_file")
    
    second_dir = first_dir / "second_dir"
    second_dir.mkdir()
    (second_dir / "third.txt").write_text("third_file_in_second_dir")

    assert tree.get(first_dir, False) == FileNode(name="first_dir", is_dir=True, children=[
        FileNode(name="a.txt", is_dir=False, children=[]),
        FileNode(name="b.txt", is_dir=False, children=[]),
        FileNode(name="second_dir", is_dir=True, children=[FileNode(name="third.txt", is_dir=False, children=[])])
        ]
    )

def test_get_dir_with_empty_child(tmp_path):
    tree = Tree()
    first_dir = tmp_path / "first_dir"
    first_dir.mkdir()
    (first_dir / "a.txt").write_text("first_file")

    second_dir = first_dir / "second_dir"
    second_dir.mkdir()
    (second_dir / "b.txt").write_text("second_file")

    empty_dir = first_dir / "empty_dir"
    empty_dir.mkdir()

    assert tree.get(first_dir, False) == FileNode(name="first_dir", is_dir=True, children=[
            FileNode(name="a.txt", is_dir=False, children=[]),
            FileNode(name="empty_dir", is_dir=True, children=[]),
            FileNode(name="second_dir", is_dir=True, children=[FileNode(name="b.txt", is_dir=False, children=[])])
        ]
    )

def test_get_onlyr_dirs(tmp_path):
    tree = Tree()
    first_dir = tmp_path / "first_dir"
    first_dir.mkdir()
    (first_dir / "a.txt").write_text("first_file")

    second_dir = first_dir / "second_dir"
    second_dir.mkdir()
    (second_dir / "b.txt").write_text("second_file")

    empty_dir = first_dir / "empty_dir"
    empty_dir.mkdir()

    assert tree.get(first_dir, True) == FileNode(name="first_dir", is_dir=True, children=[
            FileNode(name="empty_dir", is_dir=True, children=[]),
            FileNode(name="second_dir", is_dir=True, children=[])
        ]
    )

def test_filter_file():
    tree = Tree()
    file_node = FileNode(name="a.txt", is_dir=False, children=[])

    assert tree.filter_empty_nodes(file_node) is None

def test_filter__root_directory():
    tree = Tree()
    root_node = FileNode(name="root", is_dir=True, children=[])

    with pytest.raises(ValueError) as exc_info:
        tree.filter_empty_nodes(root_node)

    assert str(exc_info.value) == "Code should not be executed here!"

def test_filter_empty_nodes(tmp_path):
    tree = Tree()
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    empty_node = FileNode(name="empty", is_dir=True, children=[])

    tree.filter_empty_nodes(empty_node, empty_dir)

    assert not empty_dir.exists()

def test_filter_empty_nodes_recursive(tmp_path):
    tree = Tree()
    root = tmp_path / "root"
    root.mkdir()

    empty_dir = root / "empty_dir"
    empty_dir.mkdir()

    not_empty_dir = root / "not_empty_dir"
    not_empty_dir.mkdir()
    (not_empty_dir / "file.txt").write_text("file")

    root_node = FileNode(name="root", is_dir=True, children=[
            FileNode(name="empty_dir", is_dir=True, children=[]),
            FileNode(name="not_empty_dir", is_dir=True, children=[FileNode(name="file.txt", is_dir=False, children=[])])
        ]
    )

    tree.filter_empty_nodes(root_node, root)

    assert not empty_dir.exists()
    assert not_empty_dir.exists()
    assert (not_empty_dir / "file.txt").exists()