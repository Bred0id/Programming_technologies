import os

from tree_utils_02.size_node import FileSizeNode
from tree_utils_02.size_tree import SizeTree, BLOCK_SIZE


def test_construct_file(tmp_path):
    tree = SizeTree()
    file_path = tmp_path / "a.txt"
    file_path.write_text("hello")

    assert tree.construct_filenode(file_path, False) == FileSizeNode(name="a.txt", is_dir=False, children=[], size=os.path.getsize(file_path))


def test_construct_dir(tmp_path):
    tree = SizeTree()
    dir_path = tmp_path / "dir"
    dir_path.mkdir()

    assert tree.construct_filenode(dir_path, True) == FileSizeNode(name="dir", is_dir=True, children=[], size=BLOCK_SIZE)


def test_updats():
    tree = SizeTree()
    file_node = FileSizeNode(name="a.txt", is_dir=False, children=[], size=10)
    dir_node = FileSizeNode(name="dir", is_dir=True, children=[file_node], size=BLOCK_SIZE)

    assert tree.update_filenode(dir_node) == FileSizeNode(name="dir", is_dir=True, children=[file_node], size=BLOCK_SIZE + 10)