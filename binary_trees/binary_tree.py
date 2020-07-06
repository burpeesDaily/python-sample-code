# Copyright © 2019 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""A base class for binary trees.

Notes
-----
The module provides some custom types for type checking.
- `KeyType`: the key type for a tree node. The key must be comparable.

- `Paris`: an iterator of Key-Value pairs. Yield by traversal functions.
"""

import abc
import dataclasses

from typing import Any, Generic, Iterator, Optional, Tuple, TypeVar


class Comparable(abc.ABC):
    """Custom defined `Comparable` type for type hint."""

    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abc.abstractmethod
    def __lt__(self, other: Any) -> bool:
        pass

    def __gt__(self, other) -> bool:
        return (not self < other) and self != other

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __ge__(self, other) -> bool:
        return (not self < other)


KeyType = TypeVar("KeyType", bound=Comparable)
"""Type of a tree node key. The key must be comparable."""


Pairs = Iterator[Tuple[KeyType, Any]]
"""An iterator of Key-Value pairs. Yield by traversal functions."""


@dataclasses.dataclass
class Node(Generic[KeyType]):
    """Basic tree node class.

    Attributes
    ----------
    key : `KeyType`
        A key can be anything that is comparable.
    data : `Any`
        Any type of data.
    left : `Node`, optionalo
        The left child of the node.
    right : `Node`, optional
        The right child of the node.
    """

    key: KeyType
    data: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None


class BinaryTree(abc.ABC):
    """An abstract base class for any types of binary trees.

    This base class defines the basic properties and methods that all types of
    binary tress should provide.

    Attributes
    ----------
    root: `Optional[Node]`
        The root of the tree. The default is `None`.

    Methods
    -------
    search(key: `KeyType`)
        Search a binary tree based on the given key.

    insert(self, key: `KeyType`, data: `Any`)
        Insert data by its key into a binary tree.

    delete(key: `KeyType`)
        Delete data by its key from a binary treeW.

    Notes
    -----
    One reason to use abstract base class for all types of binary trees
    is to make sure the type of binary trees is compatable. Therefore, binary
    tree traversal can be performed on any type of binary trees.
    """

    def __init__(self):
        self.root: Optional[Node] = None

    @abc.abstractmethod
    def search(self, key: KeyType) -> Node:
        """Search data based on the given key.

        Parameters
        ----------
        key: `KeyType`
            The key associated with the data.

        Returns
        -------
        `Node`
            The found node whose key is the same as the given key.
        Note that the type of the node depends on the derived class, and
        the node type should derive from `Node`.

        Raises
        ------
        `KeyNotFoundError`
            Raised if the key does not exist.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def insert(self, key: KeyType, data: Any):
        """Insert data and its key into the binary tree.

        Parameters
        ----------
        key: `KeyType`
            The key associated with the data.

        data: `Any`
            The data to be inserted.

        Raises
        ------
        `DuplicateKeyError`
            Raised if the input data has existed in the tree.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, key: KeyType):
        """Delete the node based on the given key.

        Parameters
        ----------
        key: `KeyType`
            The key of the node to be deleted.

        Raises
        ------
        `KeyNotFoundError`
            Raised if the key does not exist.
        """
        raise NotImplementedError()

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
