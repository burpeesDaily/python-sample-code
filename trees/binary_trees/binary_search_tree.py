# Copyright © 2021, 2025 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

import dataclasses

from typing import Any, Optional

from trees import tree_exceptions


@dataclasses.dataclass
class Node:
    """Definition of Binary Search Tree Node."""

    key: Any
    data: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None


class BinarySearchTree:
    """Binary Search Tree class that supports insertion, deletion, and searching.

    Examples
    --------
    >>> from trees.binary_trees import binary_search_tree
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
    >>> tree.get_height(tree.root)
    4
    >>> tree.search(24).data
    `24`
    >>> tree.delete(15)
    """

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def __repr__(self):
        """Return the tree representation to visualize its layout."""
        return (
            f"{type(self)}, root={self.root}, "
            f"tree_height={str(self.get_height(self.root))}"
        )

    @property
    def empty(self) -> bool:
        """bool: `True` if the tree is empty; `False` otherwise.

        Notes
        -----
        The property, `empty`, is read-only.
        """
        if isinstance(self.root, Node):
            return False
        return True

    def search(self, key: Any) -> Node:
        """Look for a node by a given key.

        Parameters
        ----------
        key: `Any`
            The key associated with the data.

        Returns
        -------
        `Node`
            The node found by the given key.

        Raises
        ------
        `KeyNotFoundError`
            Raised if the key does not exist.
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

    def insert(self, key: Any, data: Any) -> None:
        """Insert a (key, data) pair into the binary search tree.

        Parameters
        ----------
        key: `Any`
            The key associated with the data.

        data: `Any`
            The data to be inserted.

        Raises
        ------
        `DuplicateKeyError`
            Raised if the key to be inserted has existed in the tree.
        """
        new_node = Node(key=key, data=data)
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

    def delete(self, key: Any) -> None:
        """Delete the node by the given key.

        Parameters
        ----------
        key: `Any`
            The key of the node to be deleted.

        Raises
        ------
        `KeyNotFoundError`
            Raised if the key does not exist.
        """
        if self.root:
            deleting_node = self.search(key=key)

            # Case 1: no child or Case 2: only one right child
            if deleting_node.left is None:
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.right
                )
            # Case 2: only one left child
            elif deleting_node.right is None:
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.left
                )
            # Case 3: wwo children
            else:
                replacing_node = self.get_leftmost(node=deleting_node.right)
                # the leftmost node is not the direct child of
                # the deleting node
                if replacing_node.parent != deleting_node:
                    self._transplant(
                        deleting_node=replacing_node,
                        replacing_node=replacing_node.right,
                    )
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node
                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node

    def get_leftmost(self, node: Node) -> Node:
        """Return the leftmost node from a given subtree.

        The key of the leftmost node is the smallest key in the given subtree.

        Parameters
        ----------
        node: `Node`
            The root of the subtree.

        Returns
        -------
        `Node`
            The node whose key is the smallest from the subtree of the given node.
        """
        current_node = node

        while current_node.left:
            current_node = current_node.left
        return current_node

    def get_height(self, node: Optional[Node]) -> int:
        """Return the height of the given node.

        Parameters
        ----------
        node: `Node`
            The node to get its height.

        Returns
        -------
        `int`
            The height of the given node.
        """
        if node is None:
            return 0

        if node.left is None and node.right is None:
            return 0

        return max(self.get_height(node.left), self.get_height(node.right)) + 1

    def _transplant(
        self,
        deleting_node: Node,
        replacing_node: Optional[Node],
    ) -> None:
        if deleting_node.parent is None:
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node
        if replacing_node:
            replacing_node.parent = deleting_node.parent
