# Copyright © 2019 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""AVL Tree."""

from dataclasses import dataclass
from typing import Any, Optional

from pyforest import tree_exceptions

from pyforest.binary_trees import binary_tree


@dataclass
class AVLNode(binary_tree.Node):
    """AVL Tree node definition."""

    left: Optional["AVLNode"] = None
    right: Optional["AVLNode"] = None
    parent: Optional["AVLNode"] = None
    height: int = 0


class AVLTree(binary_tree.BinaryTree):
    """AVL Tree.

    Attributes
    ----------
    root: `Optional[AVLNode]`
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
    get_leftmost(node: `AVLNode`)
        Return the node whose key is the smallest from the given subtree.
    get_rightmost(node: `AVLNode`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `AVLNode`)
        Return the successor node in the in-order order.
    get_predecessor(node: `AVLNode`)
        Return the predecessor node in the in-order order.
    get_height(node: `Optional[AVLNode]`)
        Return the height of the given node.

    Examples
    --------
    >>> from pyforest.binary_trees import avl_tree
    >>> tree = avl_tree.AVLTree()
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
    def search(self, key: Any) -> AVLNode:
        """Look for an AVL node by a given key.

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
        """Insert a (key, data) pair into the AVL tree.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.insert`.
        """
        temp: Optional[AVLNode] = self.root
        parent: Optional[AVLNode] = None
        while temp:
            parent = temp
            if key == temp.key:
                raise tree_exceptions.DuplicateKeyError(key=key)
            elif key < temp.key:
                temp = temp.left
            else:
                temp = temp.right

        node = AVLNode(key=key, data=data, parent=parent)

        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        temp = node
        while parent:
            parent.height = 1 + max(self.get_height(parent.left),
                                    self.get_height(parent.right))

            grandparent = parent.parent
            # grandparent is unbalanced
            if self._balance_factor(grandparent) < -1 or \
               self._balance_factor(grandparent) > 1:
                if parent == grandparent.left:
                    # Case 1
                    if temp == grandparent.left.left:
                        self._right_rotate(grandparent)
                    # Case 3
                    elif temp == grandparent.left.right:
                        self._left_rotate(parent)
                        self._right_rotate(grandparent)
                elif parent == grandparent.right:
                    # Case 2
                    if temp == grandparent.right.right:
                        self._left_rotate(grandparent)
                    # Case 4
                    elif temp == grandparent.right.left:
                        self._right_rotate(parent)
                        self._left_rotate(grandparent)
                break
            parent = parent.parent
            temp = temp.parent

    # Override
    def delete(self, key: Any):
        """Delete the node by the given key.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.delete`.
        """
        deleting_node: AVLNode = self.search(key=key)

        # No children or only one right child
        if deleting_node.left is None:
            self._transplant(deleting_node=deleting_node, replacing_node=deleting_node.right)

            if deleting_node.right:
                self._delete_fixup(fixing_node=deleting_node.right)

        # Only one left child
        elif deleting_node.right is None:
            self._transplant(deleting_node=deleting_node, replacing_node=deleting_node.left)

            if deleting_node.left:
                self._delete_fixup(fixing_node=deleting_node.left)

        # Two children
        else:
            replacing_node = self.get_leftmost(node=deleting_node.right)
            # The deleting node is not the direct parent of the minimum node.
            if replacing_node.parent != deleting_node:
                self._transplant(replacing_node, replacing_node.right)
                replacing_node.right = deleting_node.right
                replacing_node.right.parent = replacing_node

            self._transplant(deleting_node, replacing_node)
            replacing_node.left = deleting_node.left
            replacing_node.left.parent = replacing_node

            if replacing_node:
                self._delete_fixup(replacing_node)

    # Override
    def get_leftmost(self, node: AVLNode) -> AVLNode:
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
    def get_rightmost(self, node: AVLNode) -> AVLNode:
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
                      node: AVLNode) -> Optional[AVLNode]:
        """Return the successor node in the in-order order.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.get_successor`.
        """
        if node.right:
            return self.get_leftmost(node=node.right)
        parent = node.parent
        while parent and node == parent.right:
            node = parent
            parent = parent.parent
        return parent

    # Override
    def get_predecessor(self,
                        node: AVLNode) -> Optional[AVLNode]:
        """Return the predecessor node in the in-order order.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.get_predecessor`.
        """
        if node.left:
            return self.get_rightmost(node=node.left)
        parent = node.parent
        while parent and node == parent.left:
            node = parent
            parent = parent.parent
        return parent

    # Override
    def get_height(self, node: Optional[AVLNode]) -> int:
        """Return the height of the given node.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.get_height`.
        """
        if node is None:
            return -1
        return node.height

    def _left_rotate(self, node: AVLNode):
        temp = node.right
        node.right = temp.left
        if temp.left:
            temp.left.parent = node
        temp.parent = node.parent
        if node.parent is None:  # node is the root
            self.root = temp
        elif node == node.parent.left:  # node is the left child
            node.parent.left = temp
        else:  # node is the right child
            node.parent.right = temp

        temp.left = node
        node.parent = temp

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        temp.height = 1 + max(self.get_height(temp.left), self.get_height(temp.right))

    def _right_rotate(self, node: AVLNode):
        temp = node.left
        node.left = temp.right
        if temp.right:
            temp.right.parent = node
        temp.parent = node.parent
        if node.parent is None:  # node is the root
            self.root = temp
        elif node == node.parent.right:  # node is the left child
            node.parent.right = temp
        else:  # node is the right child
            node.parent.left = temp

        temp.right = node
        node.parent = temp

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        temp.height = 1 + max(self.get_height(temp.left), self.get_height(temp.right))

    def _transplant(self, deleting_node: AVLNode, replacing_node: AVLNode):

        if deleting_node.parent is None:
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node

        if replacing_node:
            replacing_node.parent = deleting_node.parent

    def _balance_factor(self, node: Optional[AVLNode]):
        if node is None:
            return -1
        return self.get_height(node.left) - self.get_height(node.right)

    # FIXME
    def _delete_fixup(self, fixing_node: AVLNode):

        while fixing_node:
            fixing_node.height = 1 + max(self.get_height(fixing_node.left), self.get_height(fixing_node.right))

            # Case the grandparent is unbalanced
            if (self._balance_factor(fixing_node) < -1) or (self._balance_factor(fixing_node) > 1):
                temp = fixing_node

                if temp.left.height > temp.right.height:
                    y = temp.left
                else:
                    y = temp.right

                if y.left.height > y.right.height:
                    z = y.left
                elif y.left.height < y.right.height:
                    z = y.right
                else:
                    if y == temp.left:
                        z = y.left
                    else:
                        z = y.right

                if y == temp.left:
                    # Case 1
                    if z == temp.left.left:
                        self._right_rotate(temp)
                    # Case 3
                    elif z == temp.left.right:
                        self._left_rotate(y)
                        self._right_rotate(temp)

                elif y == temp.right:
                    # Case 2
                    if z == temp.right.right:
                        self._left_rotate(temp)
                    # Case 4
                    elif z == temp.right.left:
                        self._right_rotate(y)
                        self._left_rotate(temp)

            fixing_node = fixing_node.parent
