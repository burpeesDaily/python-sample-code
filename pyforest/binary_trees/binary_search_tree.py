# Copyright © 2019 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Binary Search Tree."""

from typing import Any, Optional

from pyforest import tree_exceptions

from pyforest.binary_trees import binary_tree


class BinarySearchTree(binary_tree.BinaryTree):
    """Binary Search Tree.

    Attributes
    ----------
    root: `Optional[Node]`
        The root node of the binary search tree.
    empty: `bool`
        `True` if the tree is empty; `False` otherwise.

    Methods
    -------
    search(key: `Any`)
        Look for a node based on the given key.
    insert(key: `Any`, data: `Any`)
        Insert a (key, data) pair into a binary tree.
    delete(key: `Any`)
        Delete a node based on the given key from the binary tree.
    get_leftmost(node: `Node`)
        Return the node whose key is the smallest from the given subtree.
    get_rightmost(node: `Node` = `None`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `Node`)
        Return the successor node in the in-order order.
    get_predecessor(node: `Node`)
        Return the predecessor node in the in-order order.
    get_height(node: `Optional[Node]`)
        Return the height of the given node.

    Examples
    --------
    >>> from pyforest.binary_trees import binary_search_tree
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
    >>> tree.get_leftmost().key
    1
    >>> tree.get_leftmost().data
    '1'
    >>> tree.get_rightmost().key
    34
    >>> tree.get_rightmost().data
    "34"
    >>> tree.get_height(tree.root)
    4
    >>> tree.search(24).data
    `24`
    >>> tree.delete(15)
    """

    def __init__(self):
        binary_tree.BinaryTree.__init__(self)

    # Override
    def search(self, key: Any) -> binary_tree.Node:
        """Look for a node by a given key.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.search`.
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
    def insert(self, key: Any, data: Any):
        """Insert a (key, data) pair into the binary search tree.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.insert`.
        """
        new_node = binary_tree.Node(key=key, data=data)
        parent = None
        current = self.root
        while current:
            parent = current
            if new_node.key == current.key:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
            elif new_node.key < current.key:
                current = current.left
            else:
                current = current.right
        new_node.parent = parent
        # If the tree is empty
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

    # Override
    def delete(self, key: Any):
        """Delete the node by the given key.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.delete`.
        """
        if self.root:
            deleting_node = self.search(key=key)

            # Case 1: no child or Case 2: only one right child
            if deleting_node.left is None:
                self._transplant(deleting_node=deleting_node,
                                 replacing_node=deleting_node.right)
            # Case 2: only one left child
            elif deleting_node.right is None:
                self._transplant(deleting_node=deleting_node,
                                 replacing_node=deleting_node.left)
            # Case 3: wwo children
            else:
                replacing_node = \
                    self.get_leftmost(node=deleting_node.right)
                # the leftmost node is not the direct child of
                # the deleting node
                if replacing_node.parent != deleting_node:
                    self._transplant(deleting_node=replacing_node,
                                     replacing_node=replacing_node.right)
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node
                self._transplant(deleting_node=deleting_node,
                                 replacing_node=replacing_node)
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node

    # Override
    def get_leftmost(self, node: binary_tree.Node) -> binary_tree.Node:
        """Return the leftmost node from a given subtree.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.get_leftmost`.
        """
        current_node = node

        while current_node.left:
            current_node = current_node.left
        return current_node

    # Override
    def get_rightmost(self, node: binary_tree.Node) -> binary_tree.Node:
        """Return the rightmost node from a given subtree.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.get_rightmost`.
        """
        current_node = node

        if current_node:
            while current_node.right:
                current_node = current_node.right
        return current_node

    # Override
    def get_successor(self,
                      node: binary_tree.Node) -> Optional[binary_tree.Node]:
        """Return the successor node in the in-order order.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.get_successor`.
        """
        if node.right:  # Case 1: Right child is not empty
            return self.get_leftmost(node=node.right)
        # Case 2: Right child is empty
        parent = node.parent
        while parent and node == parent.right:
            node = parent
            parent = parent.parent
        return parent

    # Override
    def get_predecessor(self,
                        node: binary_tree.Node) -> Optional[binary_tree.Node]:
        """Return the predecessor node in the in-order order.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.get_predecessor`.
        """
        if node.left:  # Case 1: Left child is not empty
            return self.get_rightmost(node=node.left)
        # Case 2: Left child is empty
        parent = node.parent
        while parent and node == parent.left:
            node = parent
            parent = parent.parent
        return parent

    # Override
    def get_height(self, node: Optional[binary_tree.Node]) -> int:
        """Return the height of the given node.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.get_height`.
        """
        if node is None:
            return 0

        if node.left is None and node.right is None:
            return 0

        return max(self.get_height(node.left),
                   self.get_height(node.right)) + 1

    def _transplant(self, deleting_node: binary_tree.Node,
                    replacing_node: Optional[binary_tree.Node]):
        if deleting_node.parent is None:
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node
        if replacing_node:
            replacing_node.parent = deleting_node.parent
