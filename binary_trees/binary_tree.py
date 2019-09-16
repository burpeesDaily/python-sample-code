# Copyright © 2019 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""A base class for binary trees."""

import abc
import dataclasses
import functools

from typing import Any, Generic, NoReturn, Optional, TypeVar


@functools.total_ordering
class _Comparable(abc.ABC):
    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abc.abstractmethod
    def __lt__(self, other: Any) -> bool:
        pass

KeyType = TypeVar("KeyType", bound=_Comparable)
"""Type of a tree node key. The key must be comparable."""


@dataclasses.dataclass
class Node(Generic[KeyType]):
    """Basic tree node class.

    Attributes
    ----------
    key : `KeyType`
        A key can be anything that is comparable.
    data : `Any`
        Any type of data.
    left : `Node`, optional
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

    Methods
    -------
    search(key: `KeyType`)
        Search binary tree for a specific key.

    insert(key: `KeyType`)
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
        self.size: int = 0

    @abc.abstractmethod
    def search(self, key: KeyType) -> Any:
        """Search the data based the given key."""
        pass

    @abc.abstractmethod
    def insert(self, key: KeyType, data: Any) -> NoReturn:
        """Insert data and its key into the binary tree."""
        pass

    @abc.abstractmethod
    def delete(self, key: KeyType) -> NoReturn:
        """Delete the data based on the given key."""
        pass

    @property
    def size(self) -> int:
        """Size of a tree, i.e., the number of nodes."""
        return self._size

    @size.setter
    def size(self, value: int):
        if value < 0:
            raise ValueError("Size cannot be less than 0.")
        self._size = value

TreeType = TypeVar("TreeType", bound=BinaryTree)
"""Type of a binary tree class which must be derived from `BaseTree`"""
