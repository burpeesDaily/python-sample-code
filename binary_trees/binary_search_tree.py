# Copyright © 2019 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""A Binary Search Tree (BST) module.

A BST is a binary tree with the following properties:

- The left subtree of a node contains only nodes whose keys are less
  than or equal to the node’s key
- The right subtree of a node contains only nodes whose keys are
  greater than the node’s key

Besides, BST should provide, at least, these Basic Operations:
- Search: search an element in a tree
- Insert: insert an element in a tree
- Delete: delete an element in a tree
- Traversal: traverses a tree

A BST keeps the keys in sorted order so that the operations can use
the principle of binary search. In general, the time complexity of
a BST is as the table.

+------------+------------+-----------+
| Operations | Average    | Worst     |
+============+============+===========+
| Space      | O(n)       | O(n)      |
+------------+------------+-----------+
| Search     | O(log n)   | O(n)      |
+------------+------------+-----------+
| Insert     | O(log n)   | O(n)      |
+------------+------------+-----------+
| Delete     | O(log n)   | O(n)      |
+------------+------------+-----------+
"""

from typing import Any, Optional

from binary_trees import binary_tree
from binary_trees import tree_exceptions


class BinarySearchTree(binary_tree.BinaryTree):
    """Binary Search Tree (BST).

    Parameters
    ----------
    key: `KeyType`
        The key of the root when the tree is initialized.
        Default is `None`.
    data: `Any`
        The data of the root when the tree is initialized.
        Default is `None`.

    Attributes
    ----------
    root: `Optional[Node]`
        The root node of the binary search tree.
    empty: `bool`
        `True` if the tree is empty; `False` otherwise.

    Methods
    -------
    search(key: `KeyType`)
        Look for a node based on the given key.
    insert(key: `KeyType`, data: `Any`)
        Insert a (key, data) pair into a binary tree.
    delete(key: `KeyType`)
        Delete a node based on the given key from the binary tree.

    Examples
    --------
    >>> from binary_trees import binary_search_tree
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
    >>> tree.search(24).data
    `24`
    >>> tree.delete(15)
    """

    def __init__(self, key: binary_tree.KeyType = None, data: Any = None):
        binary_tree.BinaryTree.__init__(self)
        if key and data:
            self.root = binary_tree.Node(key=key, data=data)

    # Override
    def search(self, key: binary_tree.KeyType) -> binary_tree.Node:
        """Look for a node by a given key.

        See Also
        --------
        :py:meth:`binary_trees.binary_tree.BinaryTree.search`.
        """
        current = self.root

        while current:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:  # key > current.key:
                current = current.right
        raise tree_exceptions.KeyNotFoundError(key=key)

    # Override
    def insert(self, key: binary_tree.KeyType, data: Any):
        """Insert a (key, data) pair into the binary search tree.

        See Also
        --------
        :py:meth:`binary_trees.binary_tree.BinaryTree.insert`.
        """
        new_node = binary_tree.Node(key=key, data=data)
        parent = None
        temp = self.root
        while temp:
            parent = temp
            if new_node.key == temp.key:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
            elif new_node.key < temp.key:
                temp = temp.left
            else:
                temp = temp.right
        # If the tree is empty
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

    # Override
    def delete(self, key: binary_tree.KeyType):
        """Delete the node by the given key.

        See Also
        --------
        :py:meth:`binary_trees.binary_tree.BinaryTree.delete`.
        """
        parent: Optional[binary_tree.Node] = None
        current: Optional[binary_tree.Node] = self.root

        # Find the deleting node and its parent.
        while True:
            if current is None:
                raise tree_exceptions.KeyNotFoundError(key=key)

            if key == current.key:
                break
            else:
                parent = current

                if key < current.key:
                    current = current.left
                elif key > current.key:
                    current = current.right

        # No children
        if current.left is None and current.right is None:
            if parent is not None:
                if parent.left == current:
                    parent.left = None
                else:
                    parent.right = None
            del(current)

        # Two children
        elif current.left and current.right:
            # Find the min node on the right sub-tree
            candidate = self._delete_helper(node=current.right)

            # Copy the candidate to the deleting node
            # After the copy, the deleting node become the new node
            current.key = candidate.key
            current.data = candidate.data

            # If the min node on the right sub-tree is the replacement of the
            # deleting node, the candidate's right pointer needs to be copied.
            if current.right == candidate:
                current.right = candidate.right

            # Delete the candidate
            del(candidate)

        # One child
        else:
            # One child (left)
            if current.left and current.right is None:
                if parent is None:
                    self.root = current.left
                else:
                    if parent.left == current:
                        parent.left = current.left
                    else:
                        parent.right = current.left
            # One child (right)
            elif current.right and current.left is None:
                if parent is None:
                    self.root = current.right
                else:
                    if parent.left == current:
                        parent.left = current.right
                    else:
                        parent.right = current.right
            # Should never happen
            else:
                raise RuntimeError("Fatal error")

            del(current)

    def _delete_helper(self, node: binary_tree.Node) -> binary_tree.Node:
        """Find the minimum node, return it, and update its parent's left.

        Parameters
        ----------
        node : `binary_tree.Node`
            The root of the right sub tree of the deleting node.

        Returns
        -------
        node : `binary_tree.Node`
            The node has the minimum key of the right sub tree of the deleting
            node.
        """
        parent = node
        current = node
        # Find the node has the minimum key and its parent.
        while True:
            if current.left:
                parent = current
                current = current.left
            else:
                break

        # When the parent equals the current node, it means the current node
        # is the node which has the minimum key.
        if parent == current:
            return current
        else:
            parent.left = None
            return current
