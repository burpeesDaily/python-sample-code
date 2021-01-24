# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Threaded Binary Search Trees."""

from dataclasses import dataclass
from typing import Any, Optional

from trees import tree_exceptions

from trees.binary_trees import binary_tree


@dataclass
class SingleThreadNode(binary_tree.Node):
    """Single Threaded Tree node definition."""

    left: Optional["SingleThreadNode"] = None
    right: Optional["SingleThreadNode"] = None
    parent: Optional["SingleThreadNode"] = None
    isThread: bool = False


@dataclass
class DoubleThreadNode(binary_tree.Node):
    """Double Threaded Tree node definition."""

    left: Optional["DoubleThreadNode"] = None
    right: Optional["DoubleThreadNode"] = None
    parent: Optional["DoubleThreadNode"] = None
    leftThread: bool = False
    rightThread: bool = False


class RightThreadedBinaryTree(binary_tree.BinaryTree):
    """Right Threaded Binary Tree.

    Attributes
    ----------
    root: `Optional[SingleThreadNode]`
        The root node of the right threaded binary search tree.
    empty: `bool`
        `True` if the tree is empty; `False` otherwise.

    Methods
    -------
    search(key: `Any`)
        Look for a node based on the given key.
    insert(key: `Any`, data: `Any`)
        Insert a (key, data) pair into the tree.
    delete(key: `Any`)
        Delete a node based on the given key from the tree.
    inorder_traverse()
        In-order traversal by using the right threads.
    preorder_traverse()
        Pre-order traversal by using the right threads.
    get_leftmost(node: `SingleThreadNode`)
        Return the node whose key is the smallest from the given subtree.
    get_rightmost(node: `SingleThreadNode`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `SingleThreadNode`)
        Return the successor node in the in-order order.
    get_predecessor(node: `SingleThreadNode`)
        Return the predecessor node in the in-order order.
    get_height(node: `Optional[SingleThreadNode]`)
        Return the height of the given node.

    Examples
    --------
    >>> from trees.binary_trees import threaded_binary_tree
    >>> tree = threaded_binary_tree.RightThreadedBinaryTree()
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
    >>> [item for item in tree.inorder_traverse()]
    [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
     (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
    >>> [item for item in tree.preorder_traverse()]
    [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
     (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
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
    def search(self, key: Any) -> SingleThreadNode:
        """Look for a node by a given key.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.search`.
        """
        current = self.root
        while current:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:  # key > current.key
                if current.isThread is False:
                    current = current.right
                else:
                    break
        raise tree_exceptions.KeyNotFoundError(key=key)

    # Override
    def insert(self, key: Any, data: Any):
        """Insert a (key, data) pair into the right threaded binary tree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.insert`.
        """
        node = SingleThreadNode(key=key, data=data)
        if self.root is None:
            self.root = node
        else:

            temp = self.root

            while temp:
                # Move to left subtree
                if node.key < temp.key:
                    if temp.left:
                        temp = temp.left
                        continue
                    else:
                        temp.left = node
                        node.right = temp
                        node.isThread = True
                        node.parent = temp
                        break
                # Move to right subtree
                elif node.key > temp.key:
                    if temp.isThread is False and temp.right:
                        temp = temp.right
                        continue
                    else:
                        node.right = temp.right
                        temp.right = node
                        node.isThread = temp.isThread
                        temp.isThread = False
                        node.parent = temp
                        break
                else:
                    raise tree_exceptions.DuplicateKeyError(key=key)

    # Override
    def delete(self, key: Any):
        """Delete the node by the given key.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.delete`.
        """
        if self.root:
            deleting_node = self.search(key=key)

            # The deleting node has no child
            if deleting_node.left is None and (
                deleting_node.right is None or deleting_node.isThread
            ):
                self._transplant(deleting_node=deleting_node, replacing_node=None)

            # The deleting node has only one right child
            elif deleting_node.left is None and deleting_node.isThread is False:
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.right
                )

            # The deleting node has only one left child,
            elif deleting_node.left and deleting_node.isThread:
                predecessor = self.get_predecessor(node=deleting_node)
                if predecessor:
                    predecessor.right = deleting_node.right
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.left
                )

            # The deleting node has two children
            elif (
                deleting_node.left
                and deleting_node.right
                and deleting_node.isThread is False
            ):
                predecessor = self.get_predecessor(node=deleting_node)

                replacing_node: SingleThreadNode = self.get_leftmost(
                    node=deleting_node.right
                )

                # the minmum node is not the direct child of the deleting node
                if replacing_node.parent != deleting_node:
                    if replacing_node.isThread:
                        self._transplant(
                            deleting_node=replacing_node, replacing_node=None
                        )
                    else:
                        self._transplant(
                            deleting_node=replacing_node,
                            replacing_node=replacing_node.right,
                        )
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node
                    replacing_node.isThread = False

                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node
                if predecessor and predecessor.isThread:
                    predecessor.right = replacing_node
            else:
                raise RuntimeError("Invalid case. Should never happened")

    # Override
    def get_leftmost(self, node: SingleThreadNode) -> SingleThreadNode:
        """Return the leftmost node from a given subtree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_leftmost`.
        """
        current_node = node

        while current_node.left:
            current_node = current_node.left
        return current_node

    # Override
    def get_rightmost(self, node: SingleThreadNode) -> SingleThreadNode:
        """Return the rightmost node from a given subtree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_rightmost`.
        """
        current_node = node

        while current_node.isThread is False and current_node.right:
            current_node = current_node.right
        return current_node

    # Override
    def get_successor(self, node: SingleThreadNode) -> Optional[SingleThreadNode]:
        """Return the successor node in the in-order order.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_successor`.
        """
        if node.isThread:
            return node.right
        else:
            if node.right:
                return self.get_leftmost(node=node.right)
            # if node.right is None, it means no successor of the given node.
            return None

    # Override
    def get_predecessor(self, node: SingleThreadNode) -> Optional[SingleThreadNode]:
        """Return the predecessor node in the in-order order.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_predecessor`.
        """
        if node.left:
            return self.get_rightmost(node=node.left)
        parent = node.parent
        while parent and node == parent.left:
            node = parent
            parent = parent.parent
        return parent

    # Override
    def get_height(self, node: Optional[SingleThreadNode]) -> int:
        """Return the height of the given node.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_height`.
        """
        if node is None:
            return 0

        if node.left is None and node.isThread:
            return 0

        return max(self.get_height(node.left), self.get_height(node.right)) + 1

    def inorder_traverse(self) -> binary_tree.Pairs:
        """Use the right threads to traverse the tree in in-order order.

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree in-order traversal.
        """
        if self.root:
            current: Optional[SingleThreadNode] = self.get_leftmost(node=self.root)
            while current:
                yield (current.key, current.data)

                if current.isThread:
                    current = current.right
                else:
                    if current.right is None:
                        break
                    current = self.get_leftmost(current.right)

    def preorder_traverse(self) -> binary_tree.Pairs:
        """Use the right threads to traverse the tree in pre-order order.

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree pre-order traversal.
        """
        current = self.root
        while current:
            yield (current.key, current.data)

            if current.isThread:
                current = current.right.right
            else:
                current = current.left

    def _transplant(
        self,
        deleting_node: SingleThreadNode,
        replacing_node: Optional[SingleThreadNode],
    ):
        if deleting_node.parent is None:
            self.root = replacing_node
            if self.root:
                self.root.isThread = False
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
            if replacing_node:
                if deleting_node.isThread:
                    if replacing_node.isThread:
                        replacing_node.right = replacing_node.right
        else:  # deleting_node == deleting_node.parent.right
            deleting_node.parent.right = replacing_node
            if replacing_node:
                if deleting_node.isThread:
                    if replacing_node.isThread:
                        replacing_node.right = replacing_node.right
            else:
                deleting_node.parent.right = deleting_node.right
                deleting_node.parent.isThread = True

        if replacing_node:
            replacing_node.parent = deleting_node.parent


class LeftThreadedBinaryTree(binary_tree.BinaryTree):
    """Left Threaded Binary Tree.

    Attributes
    ----------
    root: `Optional[SingleThreadNode]`
        The root node of the left threaded binary search tree.
    empty: `bool`
        `True` if the tree is empty; `False` otherwise.

    Methods
    -------
    search(key: `Any`)
        Look for a node based on the given key.
    insert(key: `Any`, data: `Any`)
        Insert a (key, data) pair into the tree.
    delete(key: `Any`)
        Delete a node based on the given key from the tree.
    reverse_inorder_traverse()
        Reversed In-order traversal by using the left threads.
    get_leftmost(node: `SingleThreadNode`)
        Return the node whose key is the smallest from the given subtree.
    get_rightmost(node: `SingleThreadNode`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `SingleThreadNode`)
        Return the successor node in the in-order order.
    get_predecessor(node: `SingleThreadNode`)
        Return the predecessor node in the in-order order.
    get_height(node: `Optional[SingleThreadNode]`)
        Return the height of the given node.

    Examples
    --------
    >>> from trees.binary_trees import threaded_binary_tree
    >>> tree = threaded_binary_tree.LeftThreadedBinaryTree()
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
    >>> [item for item in tree.reverse_inorder_traverse()]
    [(34, "34"), (30, "30"), (24, "24"), (23, "23"), (22, "22"),
     (20, "20"), (15, "15"), (11, "11"), (7, "7"), (4, "4"), (1, "1")]
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
    def search(self, key: Any) -> SingleThreadNode:
        """Look for a node by a given key.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.search`.
        """
        current = self.root

        while current:
            if key == current.key:
                return current
            elif key < current.key:
                if current.isThread is False:
                    current = current.left
                else:
                    break
            else:  # key > current.key:
                current = current.right
        raise tree_exceptions.KeyNotFoundError(key=key)

    # Override
    def insert(self, key: Any, data: Any):
        """Insert a (key, data) pair into the left threaded binary tree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.insert`.
        """
        node = SingleThreadNode(key=key, data=data)
        if self.root is None:
            self.root = node
        else:

            temp = self.root

            while temp:
                # Move to right subtree
                if node.key > temp.key:
                    if temp.right:
                        temp = temp.right
                        continue
                    else:
                        temp.right = node
                        node.left = temp
                        node.isThread = True
                        node.parent = temp
                        break
                # Move to left subtree
                elif node.key < temp.key:
                    if temp.isThread is False and temp.left:
                        temp = temp.left
                        continue
                    else:
                        node.left = temp.left
                        temp.left = node
                        node.isThread = temp.isThread
                        temp.isThread = False
                        node.parent = temp
                        break
                else:
                    raise tree_exceptions.DuplicateKeyError(key=key)

    # Override
    def delete(self, key: Any):
        """Delete the node by the given key.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.delete`.
        """
        if self.root:
            deleting_node = self.search(key=key)

            # The deleting node has no child
            if deleting_node.right is None and (
                deleting_node.left is None or deleting_node.isThread
            ):
                self._transplant(deleting_node=deleting_node, replacing_node=None)

            # The deleting node has only one right child,
            elif deleting_node.right and deleting_node.isThread:
                successor = self.get_successor(node=deleting_node)
                if successor:
                    successor.left = deleting_node.left
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.right
                )

            # The deleting node has only one left child
            elif (deleting_node.right is None) and (deleting_node.isThread is False):
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.left
                )

            # The deleting node has two children
            elif deleting_node.right and deleting_node.left:
                replacing_node: SingleThreadNode = self.get_leftmost(
                    node=deleting_node.right
                )

                successor = self.get_successor(node=replacing_node)

                # the minmum node is not the direct child of the deleting node
                if replacing_node.parent != deleting_node:
                    if replacing_node.isThread:
                        self._transplant(
                            deleting_node=replacing_node, replacing_node=None
                        )
                    else:
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
                replacing_node.isThread = False
                if successor and successor.isThread:
                    successor.left = replacing_node
            else:
                raise RuntimeError("Invalid case. Should never happened")

    # Override
    def get_leftmost(self, node: SingleThreadNode) -> SingleThreadNode:
        """Return the leftmost node from a given subtree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_leftmost`.
        """
        current_node = node

        while current_node.left and current_node.isThread is False:
            current_node = current_node.left
        return current_node

    # Override
    def get_rightmost(self, node: SingleThreadNode) -> SingleThreadNode:
        """Return the rightmost node from a given subtree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_rightmost`.
        """
        current_node = node

        if current_node:
            while current_node.right:
                current_node = current_node.right
        return current_node

    # Override
    def get_successor(self, node: SingleThreadNode) -> Optional[SingleThreadNode]:
        """Return the successor node in the in-order order.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_successor`.
        """
        if node.right:
            return self.get_leftmost(node=node.right)
        parent = node.parent
        while parent and node == parent.right:
            node = parent
            parent = parent.parent
        return parent

    # Override
    def get_predecessor(self, node: SingleThreadNode) -> Optional[SingleThreadNode]:
        """Return the predecessor node in the in-order order.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_predecessor`.
        """
        if node.isThread:
            return node.left
        else:
            if node.left:
                return self.get_rightmost(node=node.left)
            # if node.left is None, it means no predecessor of the given node.
            return None

    # Override
    def get_height(self, node: Optional[SingleThreadNode]) -> int:
        """Return the height of the given node.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_height`.
        """
        if node is None:
            return 0

        if node.isThread and node.right is None:
            return 0

        return max(self.get_height(node.left), self.get_height(node.right)) + 1

    def reverse_inorder_traverse(self) -> binary_tree.Pairs:
        """Use the left threads to traverse the tree in reversed in-order.

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree reversed in-order traversal.
        """
        if self.root:
            current: Optional[SingleThreadNode] = self.get_rightmost(node=self.root)
            while current:
                yield (current.key, current.data)

                if current.isThread:
                    current = current.left
                else:
                    if current.left is None:
                        break
                    current = self.get_rightmost(current.left)

    def _transplant(
        self,
        deleting_node: SingleThreadNode,
        replacing_node: Optional[SingleThreadNode],
    ):
        if deleting_node.parent is None:
            self.root = replacing_node
            if self.root:
                self.root.isThread = False
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
            if replacing_node:
                if deleting_node.isThread:
                    if replacing_node.isThread:
                        replacing_node.left = deleting_node.left
            else:
                deleting_node.parent.left = deleting_node.left
                deleting_node.parent.isThread = True
        else:  # deleting_node == deleting_node.parent.right
            deleting_node.parent.right = replacing_node
            if replacing_node:
                if deleting_node.isThread:
                    if replacing_node.isThread:
                        replacing_node.left = deleting_node.left

        if replacing_node:
            replacing_node.parent = deleting_node.parent


class DoubleThreadedBinaryTree(binary_tree.BinaryTree):
    """Double Threaded Binary Tree.

    Attributes
    ----------
    root: `Optional[DoubleThreadNode]`
        The root node of the left threaded binary search tree.
    empty: `bool`
        `True` if the tree is empty; `False` otherwise.

    Methods
    -------
    search(key: `Any`)
        Look for a node based on the given key.
    insert(key: `Any`, data: `Any`)
        Insert a (key, data) pair into the tree.
    delete(key: `Any`)
        Delete a node based on the given key from the tree.
    inorder_traverse()
        In-order traversal by using the right threads.
    preorder_traverse()
        Pre-order traversal by using the right threads.
    reverse_inorder_traverse()
        Reversed In-order traversal by using the left threads.
    get_leftmost(node: `DoubleThreadNode`)
        Return the node whose key is the smallest from the given subtree.
    get_rightmost(node: `DoubleThreadNode`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `DoubleThreadNode`)
        Return the successor node in the in-order order.
    get_predecessor(node: `DoubleThreadNode`)
        Return the predecessor node in the in-order order.
    get_height(node: `Optional[DoubleThreadNode]`)
        Return the height of the given node.

    Examples
    --------
    >>> from trees.binary_trees import threaded_binary_tree
    >>> tree = threaded_binary_tree.DoubleThreadedBinaryTree()
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
    >>> [item for item in tree.inorder_traverse()]
    [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
     (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
    >>> [item for item in tree.preorder_traverse()]
    [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
     (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
    >>> [item for item in tree.reverse_inorder_traverse()]
    [(34, "34"), (30, "30"), (24, "24"), (23, "23"), (22, "22"),
     (20, "20"), (15, "15"), (11, "11"), (7, "7"), (4, "4"), (1, "1")]
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
    def search(self, key: Any) -> DoubleThreadNode:
        """Look for a node by a given key.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.search`.
        """
        current = self.root
        while current:
            if key == current.key:
                return current
            elif key < current.key:
                if current.leftThread is False:
                    current = current.left
                else:
                    break
            else:  # key > current.key
                if current.rightThread is False:
                    current = current.right
                else:
                    break
        raise tree_exceptions.KeyNotFoundError(key=key)

    # Override
    def insert(self, key: Any, data: Any):
        """Insert a (key, data) pair into the double threaded binary tree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.insert`.
        """
        node = DoubleThreadNode(key=key, data=data)
        if self.root is None:
            self.root = node
        else:

            temp = self.root

            while temp:
                # Move to left subtree
                if node.key < temp.key:
                    if temp.leftThread is False and temp.left:
                        temp = temp.left
                        continue
                    else:
                        node.left = temp.left
                        temp.left = node
                        node.right = temp
                        node.rightThread = True
                        node.parent = temp
                        temp.leftThread = False
                        if node.left:
                            node.leftThread = True
                        break
                # Move to right subtree
                elif node.key > temp.key:
                    if temp.rightThread is False and temp.right:
                        temp = temp.right
                        continue
                    else:
                        node.right = temp.right
                        temp.right = node
                        node.left = temp
                        node.leftThread = True
                        temp.rightThread = False
                        node.parent = temp
                        if node.right:
                            node.rightThread = True
                        break
                else:
                    raise tree_exceptions.DuplicateKeyError(key=key)

    # Override
    def delete(self, key: Any):
        """Delete the node by the given key.

        See Also
        --------
        :py:meth:`treesnary_trees.binary_tree.BinaryTree.delete`.
        """
        if self.root:
            deleting_node = self.search(key=key)

            # The deleting node has no child
            if (deleting_node.leftThread or deleting_node.left is None) and (
                deleting_node.rightThread or deleting_node.right is None
            ):
                self._transplant(deleting_node=deleting_node, replacing_node=None)

            # The deleting node has only one right child
            elif (
                deleting_node.leftThread or deleting_node.left is None
            ) and deleting_node.rightThread is False:

                successor = self.get_successor(node=deleting_node)
                if successor:
                    successor.left = deleting_node.left
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.right
                )

            # The deleting node has only one left child,
            elif (
                deleting_node.rightThread or deleting_node.right is None
            ) and deleting_node.leftThread is False:

                predecessor = self.get_predecessor(node=deleting_node)
                if predecessor:
                    predecessor.right = deleting_node.right
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.left
                )

            # The deleting node has two children
            elif deleting_node.left and deleting_node.right:
                predecessor = self.get_predecessor(node=deleting_node)

                replacing_node: DoubleThreadNode = self.get_leftmost(
                    node=deleting_node.right
                )

                successor = self.get_successor(node=replacing_node)

                # the minmum node is not the direct child of the deleting node
                if replacing_node.parent != deleting_node:
                    if replacing_node.rightThread:
                        self._transplant(
                            deleting_node=replacing_node, replacing_node=None
                        )
                    else:
                        self._transplant(
                            deleting_node=replacing_node,
                            replacing_node=replacing_node.right,
                        )
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node
                    replacing_node.rightThread = False

                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node
                replacing_node.leftThread = False
                if predecessor and predecessor.rightThread:
                    predecessor.right = replacing_node

                if successor and successor.leftThread:
                    successor.left = replacing_node
            else:
                raise RuntimeError("Invalid case. Should never happened")

    # Override
    def get_leftmost(self, node: DoubleThreadNode) -> DoubleThreadNode:
        """Return the leftmost node from a given subtree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_leftmost`.
        """
        current_node = node
        while current_node.left and current_node.leftThread is False:
            current_node = current_node.left
        return current_node

    # Override
    def get_rightmost(self, node: DoubleThreadNode) -> DoubleThreadNode:
        """Return the rightmost node from a given subtree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_rightmost`.
        """
        current_node = node
        if current_node:
            while current_node.right and current_node.rightThread is False:
                current_node = current_node.right
        return current_node

    # Override
    def get_successor(self, node: DoubleThreadNode) -> Optional[DoubleThreadNode]:
        """Return the successor node in the in-order order.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_successor`.
        """
        if node.rightThread:
            return node.right
        else:
            if node.right:
                return self.get_leftmost(node=node.right)
            return None

    # Override
    def get_predecessor(self, node: DoubleThreadNode) -> Optional[DoubleThreadNode]:
        """Return the predecessor node in the in-order order.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_predecessor`.
        """
        if node.leftThread:
            return node.left
        else:
            if node.left:
                return self.get_rightmost(node=node.left)
            return None

    # Override
    def get_height(self, node: Optional[DoubleThreadNode]) -> int:
        """Return the height of the given node.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_height`.
        """
        if node is None:
            return 0

        if (
            (node.left is None and node.right is None)
            or (node.leftThread and node.right is None)
            or (node.left is None and node.rightThread)
            or (node.leftThread and node.rightThread)
        ):
            return 0

        return max(self.get_height(node.left), self.get_height(node.right)) + 1

    def preorder_traverse(self) -> binary_tree.Pairs:
        """Use the right threads to traverse the tree in pre-order order.

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree pre-order traversal.
        """
        current = self.root
        while current:
            yield (current.key, current.data)

            if current.rightThread:
                current = current.right.right
            elif current.leftThread is False:
                current = current.left
            else:
                break

    def inorder_traverse(self) -> binary_tree.Pairs:
        """Use the right threads to traverse the tree in in-order order.

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree in-order traversal.
        """
        if self.root:
            current: Optional[DoubleThreadNode] = self.get_leftmost(node=self.root)
            while current:
                yield (current.key, current.data)

                if current.rightThread:
                    current = current.right
                else:
                    if current.right is None:
                        break
                    current = self.get_leftmost(current.right)

    def reverse_inorder_traverse(self) -> binary_tree.Pairs:
        """Use the left threads to traverse the tree in reversed in-order.

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree reversed in-order traversal.
        """
        if self.root:
            current: Optional[DoubleThreadNode] = self.get_rightmost(node=self.root)
            while current:
                yield (current.key, current.data)

                if current.leftThread:
                    current = current.left
                else:
                    if current.left is None:
                        break
                    current = self.get_rightmost(current.left)

    def _transplant(
        self,
        deleting_node: DoubleThreadNode,
        replacing_node: Optional[DoubleThreadNode],
    ):
        if deleting_node.parent is None:
            self.root = replacing_node
            if self.root:
                self.root.leftThread = False
                self.root.rightThread = False
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node

            if replacing_node:

                if deleting_node.leftThread:

                    if replacing_node.leftThread:
                        replacing_node.left = deleting_node.left

                if deleting_node.rightThread:

                    if replacing_node.rightThread:
                        replacing_node.right = replacing_node.right

            else:
                deleting_node.parent.left = deleting_node.left
                deleting_node.parent.leftThread = True

        else:  # deleting_node == deleting_node.parent.right
            deleting_node.parent.right = replacing_node

            if replacing_node:

                if deleting_node.leftThread:

                    if replacing_node.leftThread:
                        replacing_node.left = deleting_node.left

                if deleting_node.rightThread:

                    if replacing_node.rightThread:
                        replacing_node.right = replacing_node.right

            else:
                deleting_node.parent.right = deleting_node.right
                deleting_node.parent.rightThread = True

        if replacing_node:
            replacing_node.parent = deleting_node.parent
