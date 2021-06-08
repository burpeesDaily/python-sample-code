"""Unit tests for the AVL tree module."""

import pytest

from trees import tree_exceptions

from trees.binary_trees import avl_tree
from trees.binary_trees import traversal


def test_simple_case(basic_tree):
    """Test the basic operation of an AVL tree."""
    tree = avl_tree.AVLTree()

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert tree.get_leftmost(tree.root).key == 1
    assert tree.get_leftmost(tree.root).data == "1"
    assert tree.get_rightmost(tree.root).key == 34
    assert tree.get_rightmost(tree.root).data == "34"
    assert tree.search(24).key == 24
    assert tree.search(24).data == "24"

    tree.delete(key=15)

    with pytest.raises(tree_exceptions.KeyNotFoundError):
        tree.search(key=15)


def test_deletion(basic_tree):
    """Test the deletion of an AVL tree."""
    tree = avl_tree.AVLTree()

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    # No child
    tree.delete(15)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (20, "20"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    # One right child
    tree.delete(20)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    # One left child
    tree.insert(key=17, data="17")
    tree.delete(22)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (17, "17"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    # Two children
    tree.delete(11)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (17, "17"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]
