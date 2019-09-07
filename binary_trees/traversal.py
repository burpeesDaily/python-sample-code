# Copyright © 2019 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Binary tree traversal.

Routines
--------
inorder_traverse(
    tree: binary_tree.TreeType) -> List[Tuple[binary_tree.KeyType, Any]]
    Perform in-order traversal.

preorder_traverse(
    tree: binary_tree.TreeType) -> List[Tuple[binary_tree.KeyType, Any]]
    Perform pre-order traversal.

postorder_traverse(
    tree: binary_tree.TreeType) -> List[Tuple[binary_tree.KeyType, Any]]
    Perform post-order traversal.

levelorder_traverse(
    tree: binary_tree.TreeType) -> List[Tuple[binary_tree.KeyType, Any]]
    Perform level order traversal.
"""

from typing import Any, List, NoReturn, Optional, Tuple

from binary_trees import binary_tree


OutputType = List[Tuple[binary_tree.KeyType, Any]]
"""Output type of tree traversal."""

NodeType = Optional[binary_tree.Node]
"""Alias for the `binary_tree.Node`"""


def _inorder_traverse(node: NodeType, output: OutputType):
    """Perform In-Order traversal.

    Parameters
    ----------
    node : `NodeType`
        The root of the binary tree.

    output : `OutputType`
        The result of the traversal. This is an output parameter.
    """
    if node:
        _inorder_traverse(node.left, output)
        output.append((node.key, node.data))
        _inorder_traverse(node.right, output)


def _outorder_traverse(node: NodeType, output: OutputType):
    """Perform Output-Order traversal.

    Parameters
    ----------
    node : `NodeType`
        The root of the binary tree.

    output : `OutputType`
        The result of the traversal. This is an output parameter.
    """
    if node:
        _outorder_traverse(node.right, output)
        output.append((node.key, node.data))
        _outorder_traverse(node.left, output)


def _preorder_traverse(node: NodeType, output: OutputType):
    """Perform Pre-Order traversal.

    Parameters
    ----------
    node : `NodeType`
        The root of the binary tree.

    output : `OutputType`
        The result of the traversal. This is an output parameter.
    """
    if node:
        output.append((node.key, node.data))
        _preorder_traverse(node.left, output)
        _preorder_traverse(node.right, output)


def _postorder_traverse(node: NodeType, output: OutputType):
    """Perform Post-Order traversal.

    Parameters
    ----------
    node : `NodeType`
        The root of the binary tree.

    output : `OutputType`
        The result of the traversal. This is an output parameter.
    """
    if node:
        _postorder_traverse(node.left, output)
        _postorder_traverse(node.right, output)
        output.append((node.key, node.data))


def inorder_traverse(tree: binary_tree.TreeType) -> OutputType:
    """Perform In-Order traversal.

    In-order traversal traverses a tree by the order:
    left subtree, current node, right subtree (LDR)

    Parameters
    ----------
    tree : `binary_tree.TreeType`
        A type of binary tree.

    Returns
    -------
    inorder : `OutputType`
        Return the result of the in-order traversal.

    Examples
    --------
    >>> from binary_trees import binary_search_tree
    >>> from binary_trees import traversal
    >>> tree = binary_search_tree.BinarySearchTree()
    >>> tree.insert(key=23, data="23")
    >>> tree.insert(key=4, data="4")
    >>> tree.insert(key=30, data="30")
    >>> tree.insert(key=11, data="11")
    >>> tree.insert(key=7, data="7")
    >>> tree.insert(key=34, data="34")
    >>> tree.insert(key=20, data="20")
    >>> tree.insert(key=24, data="24")
    >>> tree.insert(key=22, data="22")
    >>> tree.insert(key=15, data="15")
    >>> tree.insert(key=1, data="1")
    >>> traversal.inorder_traverse(tree)
    [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
     (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
    >>> traversal.inorder_traverse(tree, recursive=False)
    [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
     (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
    """
    output: OutputType = []
    _inorder_traverse(node=tree.root, output=output)
    return output


def outorder_traverse(tree: binary_tree.TreeType) -> OutputType:
    """Perform Out-Order traversal.

    Out-order traversal traverses a tree by the order:
    right subtree, current node, left subtree (RNL)

    Parameters
    ----------
    tree : `binary_tree.TreeType`
        A type of binary tree.

    Returns
    -------
    outorder : `OutputType`
        Return the result of the out-order traversal.

    Examples
    --------
    >>> from binary_trees import binary_search_tree
    >>> from binary_trees import traversal
    >>> tree = binary_search_tree.BinarySearchTree()
    >>> tree.insert(key=23, data="23")
    >>> tree.insert(key=4, data="4")
    >>> tree.insert(key=30, data="30")
    >>> tree.insert(key=11, data="11")
    >>> tree.insert(key=7, data="7")
    >>> tree.insert(key=34, data="34")
    >>> tree.insert(key=20, data="20")
    >>> tree.insert(key=24, data="24")
    >>> tree.insert(key=22, data="22")
    >>> tree.insert(key=15, data="15")
    >>> tree.insert(key=1, data="1")
    >>> traversal.outorder_traverse(tree)
    [(34, '34'), (30, '30'), (24, '24'), (23, '23'), (22, '22'), (20, '20'),
     (15, '15'), (11, '11'), (7, '7'), (4, '4'), (1, '1')]
    >>> traversal.outorder_traverse(tree, recursive=False)
    [(34, '34'), (30, '30'), (24, '24'), (23, '23'), (22, '22'), (20, '20'),
     (15, '15'), (11, '11'), (7, '7'), (4, '4'), (1, '1')]
    """
    output: OutputType = []
    _outorder_traverse(node=tree.root, output=output)
    return output


def preorder_traverse(tree: binary_tree.TreeType) -> OutputType:
    """Perform Pre-Order traversal.

    Pre-order traversal traverses a tree by the order:
    current node, left subtree, right subtree (DLR)

    Parameters
    ----------
    tree : `binary_tree.TreeType`
        A type of binary tree.

    Returns
    -------
    preorder : `OutputType`
        Return the result of the pre-order traversal.

    Examples
    --------
    >>> from binary_trees import binary_search_tree
    >>> from binary_trees import traversal
    >>> tree = binary_search_tree.BinarySearchTree()
    >>> tree.insert(key=23, data="23")
    >>> tree.insert(key=4, data="4")
    >>> tree.insert(key=30, data="30")
    >>> tree.insert(key=11, data="11")
    >>> tree.insert(key=7, data="7")
    >>> tree.insert(key=34, data="34")
    >>> tree.insert(key=20, data="20")
    >>> tree.insert(key=24, data="24")
    >>> tree.insert(key=22, data="22")
    >>> tree.insert(key=15, data="15")
    >>> tree.insert(key=1, data="1")
    >>> traversal.preorder_traverse(tree)
    [(23, '23'), (4, '4'), (1, '1'), (11, '11'), (7, '7'), (20, '20'),
     (15, '15'), (22, '22'), (30, '30'), (24, '24'), (34, '34')]
    >>> traversal.preorder_traverse(tree, recursive=False)
    [(23, '23'), (4, '4'), (1, '1'), (11, '11'), (7, '7'), (20, '20'),
     (15, '15'), (22, '22'), (30, '30'), (24, '24'), (34, '34')]
    """
    output: OutputType = []
    _preorder_traverse(node=tree.root, output=output)
    return output


def postorder_traverse(tree: binary_tree.TreeType) -> OutputType:
    """Perform Post-Order traversal.

    Post-order traversal traverses a tree by the order:
    left subtree, right subtree, current node (LRD)

    Parameters
    ----------
    tree : `binary_tree.TreeType`
        A type of binary tree.

    Returns
    -------
    postorder : `OutputType`
        Return the result of the post-order traversal.

    Examples
    --------
    >>> from binary_trees import binary_search_tree
    >>> from binary_trees import traversal
    >>> tree = binary_search_tree.BinarySearchTree()
    >>> tree.insert(key=23, data="23")
    >>> tree.insert(key=4, data="4")
    >>> tree.insert(key=30, data="30")
    >>> tree.insert(key=11, data="11")
    >>> tree.insert(key=7, data="7")
    >>> tree.insert(key=34, data="34")
    >>> tree.insert(key=20, data="20")
    >>> tree.insert(key=24, data="24")
    >>> tree.insert(key=22, data="22")
    >>> tree.insert(key=15, data="15")
    >>> tree.insert(key=1, data="1")
    >>> traversal.postorder_traverse(tree)
    [(1, '1'), (7, '7'), (15, '15'), (22, '22'), (20, '20'), (11, '11'),
     (4, '4'), (24, '24'), (34, '34'), (30, '30'), (23, '23')]
    >>> traversal.postorder_traverse(tree, recursive=False)
    [(1, '1'), (7, '7'), (15, '15'), (22, '22'), (20, '20'), (11, '11'),
     (4, '4'), (24, '24'), (34, '34'), (30, '30'), (23, '23')]
    """
    output: OutputType = []
    _postorder_traverse(node=tree.root, output=output)
    return output


def levelorder_traverse(tree: binary_tree.TreeType) -> OutputType:
    """Perform Level-Order traversal.

    Level-order traversal traverses a tree:
    level by level, from left to right, starting from the root node.

    Parameters
    ----------
    tree : `binary_tree.TreeType`
        A type of binary tree.

    Returns
    -------
    levelorder : `OutputType`
        Return the result of the level-order traversal.

    Examples
    --------
    >>> from binary_trees import binary_search_tree
    >>> from binary_trees import traversal
    >>> tree = binary_search_tree.BinarySearchTree()
    >>> tree.insert(key=23, data="23")
    >>> tree.insert(key=4, data="4")
    >>> tree.insert(key=30, data="30")
    >>> tree.insert(key=11, data="11")
    >>> tree.insert(key=7, data="7")
    >>> tree.insert(key=34, data="34")
    >>> tree.insert(key=20, data="20")
    >>> tree.insert(key=24, data="24")
    >>> tree.insert(key=22, data="22")
    >>> tree.insert(key=15, data="15")
    >>> tree.insert(key=1, data="1")
    >>> traversal.levelorder_traverse(tree)
    [(23, '23'), (4, '4'), (30, '30'), (1, '1'), (11, '11'), (24, '24'),
     (34, '34'), (7, '7'), (20, '20'), (15, '15'), (22, '22')]
    """
    queue = [tree.root]
    output: OutputType = []

    while len(queue) > 0:
        temp = queue.pop(0)
        if temp is not None:
            output.append((temp.key, temp.data))
            if temp.left:
                queue.append(temp.left)

            if temp.right:
                queue.append(temp.right)

    return output
