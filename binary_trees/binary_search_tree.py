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

from typing import Any, Generic, NoReturn, Optional

from binary_trees import binary_tree
from binary_trees import traversal


class BinarySearchTree(binary_tree.BinaryTree):
    """Binary Search Tree (BST) class.

    Attributes
    ----------
    root : `binary_tree.Node`
        The root o   the binary search tree.

    Methods
    -------
    delete(key: binary_tree.KeyType)
        Delete the data from a tree based on the key.
    get_height()
        Return the height of the tree.
    get_max()
        Return the maximum key from the tree.
    get_min()
        Return the minimum key from the tree.
    insert(key: binary_tree.KeyType, data: Any)
        Insert a key and data pair into a tree.
    is_balance()
        Check if the tree is balance.
    search(key: binary_tree.KeyType)
        Look for the key in a tree.
    size()
        Return the total number of nodes of the tree.

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
    >>> tree.size()
    11
    >>> tree.get_min()
    1
    >>> tree.get_max()
    34
    >>> tree.get_height()
    4
    >>> tree.is_balance()
    False
    >>> tree.search(24)
    24
    >>> tree.delete(15)
    """

    def __init__(self, key: binary_tree.KeyType = None, data: Any = None):
        binary_tree.BinaryTree.__init__(self)
        if key and data:
            self.root = binary_tree.Node(key=key, data=data)
            self.size = 1

    def _insert(self,
                key: binary_tree.KeyType,
                data: Any,
                node: binary_tree.Node):
        """Real implementation of tree insertion.

        Parameters
        ----------
        key : `binary_tree.KeyType`
            The key of the data.
        data : `Any`
            The data to be inserted into the tree.
        node : `binary_tree.Node`
            The parent node of the input data.

        Raises
        ------
        ValueError
            If the input data has existed in the tree, `ValueError`
            will be thrown.
        """
        if key == node.key:
            raise ValueError("Duplicate key")
        elif key < node.key:
            if node.left is not None:
                self._insert(key=key, data=data, node=node.left)
            else:
                node.left = binary_tree.Node(key=key, data=data)
        else:  # key > node.key
            if node.right is not None:
                self._insert(key=key, data=data, node=node.right)
            else:
                node.right = binary_tree.Node(key=key, data=data)

    def _search(self,
                key: binary_tree.KeyType,
                node: binary_tree.Node) -> binary_tree.Node:
        """Real implementation of search.

        Parameters
        ----------
        key : `binary_tree.KeyType`
            The key of the data.
        node : `binary_tree.Node`
            The node to check if its key matches the given key.

        Retruns
        -------
        node : `binary_tree.Node`
            Return the node if the key matches, or the node for next recursion.

        Raises
        ------
        KeyError
            If the key does not exist, `KeyError` will be thrown.
        """
        if key == node.key:
            return node
        elif key < node.key:
            if node.left is not None:
                return self._search(key=key, node=node.left)
            else:
                raise KeyError(f"Key {key} not found")
        else:  # key > node.key
            if node.right is not None:
                return self._search(key=key, node=node.right)
            else:
                raise KeyError(f"Key {key} not found")

    def _get_min(self, node: binary_tree.Node) -> binary_tree.Node:
        """Real implementation of getting the leftmost node.

        Parameters
        ----------
        node : `binary_tree.Node`
            The root of the tree.

        Retruns
        -------
        node : `binary_tree.Node`
            Return the leftmost node in the tree.
        """
        current_node = node
        while current_node.left:
            current_node = current_node.left
        return current_node

    def _height(self, node: Optional[binary_tree.Node]) -> int:
        """Real implementation of getting the height of a given node.

        Parameters
        ----------
        node : `binary_tree.Node`, optional
            The root of the tree.

        Retruns
        -------
        height : `int`
            Return the height of the given node.
        """
        if node is None:
            return 0

        if node.left is None and node.right is None:
            return 0

        return max(self._height(node.left), self._height(node.right)) + 1

    def _is_balance(self, node: binary_tree.Node) -> bool:
        """Real implementation of checking if a tree is balance.

        Parameters
        ----------
        node : `binary_tree.Node`
            The root of the tree.

        Retruns
        -------
        balance : `bool`
            Return True if the tree is balance; False otherwise.
        """
        left_hight = self._height(node.left)
        right_height = self._height(node.right)

        if (abs(left_hight - right_height) > 1):
            return False

        if node.left:
            if not self._is_balance(node=node.left):
                return False
        if node.right:
            if not self._is_balance(node=node.right):
                return False

        return True

    # Overriding abstract method
    def search(self, key: binary_tree.KeyType) -> Any:
        """Search data based on the given key.

        Parameters
        ----------
        key : `binary_tree.KeyType`
            The key associated with the data.

        Returns
        -------
        data : `Any`
            The data based on the given key; None if the key not found.

        Raises
        ------
        KeyError
            If the key does not exist, `KeyError` will be thrown.
        """
        if self.size == 0 or self.root is None:
            return None

        return self._search(key=key, node=self.root).data

    # Overriding abstract method
    def insert(self, key: binary_tree.KeyType, data: Any):
        """Insert data and its key into the binary tree.

        Parameters
        ----------
        key : `binary_tree.KeyType`
            A unique key associated with the data.

        data : `Any`
            The data to be inserted into the tree.

        Raises
        ------
        ValueError
            If the input data has existed in the tree, `ValueError`
            will be thrown.
        """
        if self.size == 0 or self.root is None:
            self.root = binary_tree.Node(key=key, data=data)
        else:
            self._insert(key=key, data=data, node=self.root)

        self.size += 1

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

    # Overriding abstract method
    def delete(self, key: binary_tree.KeyType):
        """Delete the data based on the given key.

        Parameters
        ----------
        key : `KeyType`
            The key associated with the data.

        Raises
        ------
        KeyError
            If the key does not exist, `KeyError` will be thrown.

        RuntimeError
            Should never happen, but it happens, `RuntimeError` will be thrown.
        """
        parent: Optional[binary_tree.Node] = None
        current: Optional[binary_tree.Node] = self.root

        # Find the deleting node and its parent.
        while True:
            if current is None:
                raise KeyError("Key {key} not found")

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

        self._size -= 1

    def get_min(self) -> Any:
        """Return the minimum key from the tree."""
        if self.size == 0 or self.root is None:
            return None
        return self._get_min(self.root).key

    def get_max(self) -> Any:
        """Return the maximum key from the tree."""
        if self.size == 0 or self.root is None:
            return None

        node: binary_tree.Node = self.root

        while node.right is not None:
            node = node.right

        return node.key

    def get_height(self) -> int:
        """Return the height of the tree."""
        return self._height(self.root)

    def is_balance(self) -> bool:
        """Check if the tree is balance.

        Returns
        -------
        `bool`
            True is the tree is balance; False otherwise.
        """
        if self.size == 0 or self.root is None:
            return True

        return self._is_balance(node=self.root)


def is_valid_binary_search_tree(tree: binary_tree.TreeType):
    """Check if a binary tree is a valid BST.

    Parameters
    ----------
    tree : binary_tree.TreeType
        A type of binary tree.

    Returns
    -------
    bool
        True is the tree is a BST; False otherwise.

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
    >>> binary_search_tree.is_valid_binary_search_tree(tree)
    True
    """
    in_order_result = traversal.inorder_traverse(tree=tree)

    for index in range(len(in_order_result) - 1):
        if in_order_result[index] > in_order_result[index + 1]:
            return False
    return True
