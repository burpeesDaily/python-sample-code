# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Red-Black Tree."""

import enum

from dataclasses import dataclass
from typing import Any, Union, override

from trees import tree_exceptions
from trees.binary_trees import binary_tree


class Color(enum.Enum):
    """Color definition for Red-Black Tree."""

    RED = enum.auto()
    BLACK = enum.auto()


@dataclass
class LeafNode(binary_tree.Node):
    """Definition Red-Black Tree Leaf node whose color is always black."""

    left = None
    right = None
    parent = None
    color = Color.BLACK


@dataclass
class RBNode(binary_tree.Node):
    """Red-Black Tree non-leaf node definition."""

    left: Union["RBNode", LeafNode]
    right: Union["RBNode", LeafNode]
    parent: Union["RBNode", LeafNode]
    color: Color = Color.RED


class RBTree(binary_tree.BinaryTree):
    """Red-Black Tree.

    Attributes
    ----------
    root: `Union[RBNode, LeafNode]`
        The root node of the right threaded binary search tree.
    empty: `bool`
        `True` if the tree is `LeafNode`; `False` otherwise.

    Methods
    -------
    search(key: `Any`)
        Look for a node based on the given key.
    insert(key: `Any`, data: `Any`)
        Insert a (key, data) pair into the tree.
    delete(key: `Any`)
        Delete a node based on the given key from the tree.
    inorder_traverse()
        Perform In-order traversal.
    preorder_traverse()
        Perform Pre-order traversal.
    postorder_traverse()
        Perform Post-order traversal.
    get_leftmost(node: `RBNode`)
        Return the node whose key is the smallest from the given subtree.
    get_rightmost(node: `RBNode`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `RBNode`)
        Return the successor node in the in-order order.
    get_predecessor(node: `RBNode`)
        Return the predecessor node in the in-order order.
    get_height(node: `Optional[RBNode]`)
        Return the height of the given node.

    Examples
    --------
    >>> from trees.binary_trees import red_black_tree
    >>> tree = red_black_tree.RBTree()
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
        self._NIL: LeafNode = LeafNode(key=None, data=None)
        self.root: Union[RBNode, LeafNode] = self._NIL

    @override
    def search(self, key: Any) -> RBNode:
        """Look for a node by a given key.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.search`.
        """
        temp: Union[RBNode, LeafNode] = self.root
        while isinstance(temp, RBNode):
            if key < temp.key:
                temp = temp.left
            elif key > temp.key:
                temp = temp.right
            else:  # Key found
                return temp
        raise tree_exceptions.KeyNotFoundError(key=key)

    @override
    def insert(self, key: Any, data: Any):
        """Insert a (key, data) pair into the Red-Black tree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.insert`.
        """
        node = RBNode(
            key=key,
            data=data,
            left=self._NIL,
            right=self._NIL,
            parent=self._NIL,
            color=Color.RED,
        )  # Color the new node as red.
        parent: Union[RBNode, LeafNode] = self._NIL
        temp: Union[RBNode, LeafNode] = self.root
        while isinstance(temp, RBNode):  # Look for the insert location
            parent = temp
            if node.key < temp.key:
                temp = temp.left
            else:
                temp = temp.right
        # If the parent is a LeafNode, set the new node to be the root.
        if isinstance(parent, LeafNode):
            node.color = Color.BLACK
            self.root = node
        else:
            node.parent = parent

            if node.key < parent.key:
                parent.left = node
            else:
                parent.right = node

            # After the insertion, fix the broken red-black-tree-properties.
            self._insert_fixup(node)

    @override
    def delete(self, key: Any):
        """Delete the node by the given key.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.delete`.
        """
        deleting_node: RBNode = self.search(key=key)

        original_color = deleting_node.color

        # No children or only one right child
        if isinstance(deleting_node.left, LeafNode):
            replacing_node = deleting_node.right
            self._transplant(deleting_node=deleting_node, replacing_node=replacing_node)
            # Fixup
            if original_color == Color.BLACK:
                if isinstance(replacing_node, RBNode):
                    self._delete_fixup(fixing_node=replacing_node)

        # Only one left child
        elif isinstance(deleting_node.right, LeafNode):
            replacing_node = deleting_node.left
            self._transplant(deleting_node=deleting_node, replacing_node=replacing_node)
            # Fixup
            if original_color == Color.BLACK:
                self._delete_fixup(fixing_node=replacing_node)

        # Two children
        else:
            replacing_node = self.get_leftmost(deleting_node.right)
            original_color = replacing_node.color
            replacing_replacement = replacing_node.right
            # The replacing node is not the direct child of the deleting node
            if replacing_node.parent != deleting_node:
                self._transplant(replacing_node, replacing_node.right)
                replacing_node.right = deleting_node.right
                replacing_node.right.parent = replacing_node

            self._transplant(deleting_node, replacing_node)
            replacing_node.left = deleting_node.left
            replacing_node.left.parent = replacing_node
            replacing_node.color = deleting_node.color
            # Fixup
            if original_color == Color.BLACK:
                if isinstance(replacing_replacement, RBNode):
                    self._delete_fixup(fixing_node=replacing_replacement)

    @override
    def get_leftmost(self, node: RBNode) -> RBNode:
        """Return the leftmost node from a given subtree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_leftmost`.
        """
        current_node = node
        while isinstance(current_node.left, RBNode):
            current_node = current_node.left
        return current_node

    @override
    def get_rightmost(self, node: RBNode) -> RBNode:
        """Return the rightmost node from a given subtree.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_rightmost`.
        """
        current_node = node
        while isinstance(current_node.right, RBNode):
            current_node = current_node.right
        return current_node

    @override
    def get_successor(self, node: RBNode) -> Union[RBNode, LeafNode]:
        """Return the successor node in the in-order order.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_successor`.
        """
        if isinstance(node.right, RBNode):
            return self.get_leftmost(node=node.right)
        parent = node.parent
        while isinstance(parent, RBNode) and node == parent.right:
            node = parent
            parent = parent.parent
        return parent

    @override
    def get_predecessor(self, node: RBNode) -> Union[RBNode, LeafNode]:
        """Return the predecessor node in the in-order order.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_predecessor`.
        """
        if isinstance(node.left, RBNode):
            return self.get_rightmost(node=node.left)
        parent = node.parent
        while isinstance(parent, RBNode) and node == parent.left:
            node = parent
            parent = parent.parent
        return node.parent

    @override
    def get_height(self, node: Union[None, LeafNode, RBNode]) -> int:
        """Return the height of the given node.

        See Also
        --------
        :py:meth:`trees.binary_trees.binary_tree.BinaryTree.get_height`.
        """
        if node is None:
            return 0

        if isinstance(node.left, LeafNode) and isinstance(node.right, LeafNode):
            return 0

        return max(self.get_height(node.left), self.get_height(node.right)) + 1

    def inorder_traverse(self) -> binary_tree.Pairs:
        """Perform In-Order traversal.

        In-order traversal traverses a tree by the order:
        left subtree, current node, right subtree (LDR)

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the in-order traversal.

        Examples
        --------
        >>> from trees.binary_trees import red_black_tree
        >>> tree = red_black_tree.RBTree()
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
        >>> [item for item in tree.preorder_traverse()]
        [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
        (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
        """
        return self._inorder_traverse(node=self.root)  # type: ignore

    def preorder_traverse(self) -> binary_tree.Pairs:
        """Perform Pre-Order traversal.

        Pre-order traversal traverses a tree by the order:
        current node, left subtree, right subtree (DLR)

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the pre-order traversal.

        Examples
        --------
        >>> from trees.binary_trees import red_black_tree
        >>> tree = red_black_tree.RBTree()
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
        >>> [item for item in tree.preorder_traverse()]
        [(20, "20"), (7, "7"), (4, "4"), (1, "1"), (11, "11"), (15, "15"),
        (23, "23"), (22, "22"), (30, "30"), (24, "24"), (34, "34")]
        """
        return self._preorder_traverse(node=self.root)  # type: ignore

    def postorder_traverse(self) -> binary_tree.Pairs:
        """Perform Post-Order traversal.

        Post-order traversal traverses a tree by the order:
        left subtree, right subtree, current node (LRD)

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the post-order traversal.

        Examples
        --------
        >>> from trees.binary_trees import red_black_tree
        >>> tree = red_black_tree.RBTree()
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
        >>> [item for item in tree.postorder_traverse()]
        [(1, "1"), (4, "4"), (15, "15"), (11, "11"), (7, "7"), (22, "22"),
        (24, "24"), (34, "34"), (30, "30"), (23, "23"), (20, "20")]
        """
        return self._postorder_traverse(node=self.root)  # type: ignore

    def _left_rotate(self, node_x: RBNode):
        node_y = node_x.right  # Set node y
        if isinstance(node_y, LeafNode):  # Node y cannot be a LeafNode
            raise RuntimeError("Invalid left rotate")

        # Turn node y's subtree into node x's subtree
        node_x.right = node_y.left
        if isinstance(node_y.left, RBNode):
            node_y.left.parent = node_x
        node_y.parent = node_x.parent

        # If node's parent is a LeafNode, node y becomes the new root.
        if isinstance(node_x.parent, LeafNode):
            self.root = node_y
        # Otherwise, update node x's parent.
        elif node_x == node_x.parent.left:
            node_x.parent.left = node_y
        else:
            node_x.parent.right = node_y

        node_y.left = node_x
        node_x.parent = node_y

    def _right_rotate(self, node_x: RBNode):
        node_y = node_x.left  # Set node y
        if isinstance(node_y, LeafNode):  # Node y cannot be a LeafNode
            raise RuntimeError("Invalid right rotate")
        # Turn node y's subtree into node x's subtree
        node_x.left = node_y.right
        if isinstance(node_y.right, RBNode):
            node_y.right.parent = node_x
        node_y.parent = node_x.parent

        # If node's parent is a LeafNode, node y becomes the new root.
        if isinstance(node_x.parent, LeafNode):
            self.root = node_y
        # Otherwise, update node x's parent.
        elif node_x == node_x.parent.right:
            node_x.parent.right = node_y
        else:
            node_x.parent.left = node_y

        node_y.right = node_x
        node_x.parent = node_y

    def _insert_fixup(self, fixing_node: RBNode):
        while fixing_node.parent.color == Color.RED:
            if fixing_node.parent == fixing_node.parent.parent.left:  # type: ignore
                parent_sibling = fixing_node.parent.parent.right  # type: ignore
                # Case 1
                if parent_sibling.color == Color.RED:  # type: ignore
                    fixing_node.parent.color = Color.BLACK
                    parent_sibling.color = Color.BLACK  # type: ignore
                    fixing_node.parent.parent.color = Color.RED  # type: ignore
                    fixing_node = fixing_node.parent.parent  # type: ignore
                else:
                    # Case 2
                    if fixing_node == fixing_node.parent.right:  # type: ignore
                        fixing_node = fixing_node.parent  # type: ignore
                        self._left_rotate(fixing_node)
                    # Case 3
                    fixing_node.parent.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED  # type: ignore
                    self._right_rotate(fixing_node.parent.parent)  # type: ignore
            else:
                parent_sibling = fixing_node.parent.parent.left  # type: ignore
                # Case 4
                if parent_sibling.color == Color.RED:  # type: ignore
                    fixing_node.parent.color = Color.BLACK
                    parent_sibling.color = Color.BLACK  # type: ignore
                    fixing_node.parent.parent.color = Color.RED  # type: ignore
                    fixing_node = fixing_node.parent.parent  # type: ignore
                else:
                    # Case 5
                    if fixing_node == fixing_node.parent.left:  # type: ignore
                        fixing_node = fixing_node.parent  # type: ignore
                        self._right_rotate(fixing_node)
                    # Case 6
                    fixing_node.parent.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED  # type: ignore
                    self._left_rotate(fixing_node.parent.parent)  # type: ignore

        self.root.color = Color.BLACK

    def _delete_fixup(self, fixing_node: Union[LeafNode, RBNode]):
        while (fixing_node is not self.root) and (fixing_node.color == Color.BLACK):
            if fixing_node == fixing_node.parent.left:  # type: ignore
                sibling = fixing_node.parent.right  # type: ignore

                # Case 1: the sibling is red.
                if sibling.color == Color.RED:  # type: ignore
                    sibling.color == Color.BLACK  # type: ignore
                    fixing_node.parent.color = Color.RED  # type: ignore
                    self._left_rotate(fixing_node.parent)  # type: ignore
                    sibling = fixing_node.parent.right  # type: ignore

                if isinstance(sibling, LeafNode):
                    break

                # Case 2: the sibling is black and its children are black.
                if (sibling.left.color == Color.BLACK) and (  # type: ignore
                    sibling.right.color == Color.BLACK  # type: ignore
                ):
                    sibling.color = Color.RED  # type: ignore
                    # new fixing node
                    fixing_node = fixing_node.parent  # type: ignore

                # Cases 3 and 4: the sibling is black and one of
                # its child is red and the other is black.
                else:
                    # Case 3: the sibling is black and its left child is red.
                    if sibling.right.color == Color.BLACK:  # type: ignore
                        sibling.left.color = Color.BLACK  # type: ignore
                        sibling.color = Color.RED  # type: ignore
                        self._right_rotate(node_x=sibling)  # type: ignore

                    # Case 4: the sibling is black and its right child is red.
                    sibling.color = fixing_node.parent.color  # type: ignore
                    fixing_node.parent.color = Color.BLACK  # type: ignore
                    sibling.right.color = Color.BLACK  # type: ignore
                    self._left_rotate(node_x=fixing_node.parent)  # type: ignore
                    # Once we are here, all the violation has been fixed, so
                    # move to the root to terminate the loop.
                    fixing_node = self.root
            else:
                sibling = fixing_node.parent.left  # type: ignore

                # Case 5: the sibling is red.
                if sibling.color == Color.RED:  # type: ignore
                    sibling.color == Color.BLACK  # type: ignore
                    fixing_node.parent.color = Color.RED  # type: ignore
                    self._right_rotate(node_x=fixing_node.parent)  # type: ignore
                    sibling = fixing_node.parent.left  # type: ignore

                if isinstance(sibling, LeafNode):
                    break

                # Case 6: the sibling is black and its children are black.
                if (sibling.right.color == Color.BLACK) and (  # type: ignore
                    sibling.left.color == Color.BLACK  # type: ignore
                ):
                    sibling.color = Color.RED  # type: ignore
                    fixing_node = fixing_node.parent  # type: ignore
                else:
                    # Case 7: the sibling is black and its right child is red.
                    if sibling.left.color == Color.BLACK:  # type: ignore
                        sibling.right.color = Color.BLACK  # type: ignore
                        sibling.color = Color.RED  # type: ignore
                        self._left_rotate(node_x=sibling)  # type: ignore
                    # Case 8: the sibling is black and its left child is red.
                    sibling.color = fixing_node.parent.color  # type: ignore
                    fixing_node.parent.color = Color.BLACK  # type: ignore
                    sibling.left.color = Color.BLACK  # type: ignore
                    self._right_rotate(node_x=fixing_node.parent)  # type: ignore
                    # Once we are here, all the violation has been fixed, so
                    # move to the root to terminate the loop.
                    fixing_node = self.root

        fixing_node.color = Color.BLACK

    def _transplant(
        self, deleting_node: RBNode, replacing_node: Union[RBNode, LeafNode]
    ):
        if isinstance(deleting_node.parent, LeafNode):
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node

        replacing_node.parent = deleting_node.parent

    def _inorder_traverse(self, node: Union[RBNode, LeafNode]):
        if isinstance(node, RBNode):
            yield from self._inorder_traverse(node.left)
            yield (node.key, node.data)
            yield from self._inorder_traverse(node.right)

    def _preorder_traverse(self, node: Union[RBNode, LeafNode]):
        if isinstance(node, RBNode):
            yield (node.key, node.data)
            yield from self._preorder_traverse(node.left)
            yield from self._preorder_traverse(node.right)

    def _postorder_traverse(self, node: Union[RBNode, LeafNode]):
        if isinstance(node, RBNode):
            yield from self._postorder_traverse(node.left)
            yield from self._postorder_traverse(node.right)
            yield (node.key, node.data)
