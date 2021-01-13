# Copyright © 2020 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""A simple CLI application."""

import cmd

from typing import Optional

from trees.binary_trees import avl_tree
from trees.binary_trees import binary_search_tree
from trees.binary_trees import binary_tree
from trees.binary_trees import red_black_tree
from trees.binary_trees import threaded_binary_tree
from trees.binary_trees import traversal

from trees import tree_exceptions


class cli(cmd.Cmd):
    """A CLI for operating tree data structures."""

    intro = "Welcome to the Tree CLI. Type help or ? to list commands.\n"
    prompt = "tree> "

    def __init__(self):
        cmd.Cmd.__init__(self)
        self._tree: Optional[binary_tree.BinaryTree] = None

    def do_build(self, line):
        """Build a binary tree.

        Options: avl-tree, bst, rb-tree, threaded-bst
        Example:
        tree> build avl-tree
        """
        try:
            if self._tree is not None:
                print(f"Tree {type(self._tree)} already exist")
                return

            tree_type = self._get_single_arg(line=line).lower()

            if tree_type == "avl-tree":
                self._tree = avl_tree.AVLTree()
            elif tree_type == "bst":
                self._tree = binary_search_tree.BinarySearchTree()
            elif tree_type == "rb-tree":
                self._tree = red_black_tree.RBTree()
            elif tree_type == "threaded-bst":
                threaded_type = input(
                    "Please input threaded type " "(left, right, or double): "
                ).lower()
                if threaded_type == "left":
                    self._tree = threaded_binary_tree.LeftThreadedBinaryTree()
                elif threaded_type == "right":
                    self._tree = threaded_binary_tree.RightThreadedBinaryTree()
                elif threaded_type == "double":
                    self._tree = \
                        threaded_binary_tree.DoubleThreadedBinaryTree()
                else:
                    print(f"{threaded_type} is an invalid threaded type")
            else:
                print(f"{tree_type} is an invalid tree type")
        except KeyError as error:
            print(error)

    def do_search(self, line):
        """Search data by a given key.

        Example:
        tree> search 3
        """
        try:
            key = self._get_key(line=line)
            output = self._tree.search(key=key)
            print(output.key, output.data)
        except tree_exceptions.KeyNotFoundError:
            print(f"{key} does not exist")
        except KeyError as error:
            print(error)

    def do_insert(self, line):
        """Insert a (key, data) pair. The key must be an integer.

        Example:
        tree> insert 7 data
        """
        args = line.split()
        if len(args) != 2:
            print("Invalid number of the arguments")
            return

        try:
            key = self._get_key(line)
            self._tree.insert(key=key, data=args[1])
            print(f"{args[0]} and {args[1]} inserted")
        except tree_exceptions.DuplicateKeyError:
            print(f"{key} already exists")
        except KeyError as error:
            print(error)

    def do_delete(self, line):
        """Delete an item by the given key.

        Example:
        tree> delete 5
        """
        try:
            key = self._get_key(line=line)
            self._tree.delete(key=key)
            print(f"{key} removed")
        except tree_exceptions.KeyNotFoundError:
            print(f"{key} does not exist")
        except KeyError as error:
            print(error)

    def do_traverse(self, line):
        """Traverse the binary search tree.

        Options: pre, in, post, rev-in
        Example:
        tree> traverse pre
        """
        try:
            arg = self._get_single_arg(line=line).lower()

            if isinstance(self._tree, red_black_tree.RBTree):
                if arg == "pre":
                    for item in self._tree.preorder_traverse():
                        print(item)
                elif arg == "in":
                    for item in self._tree.inorder_traverse():
                        print(item)
                elif arg == "post":
                    for item in self._tree.postorder_traverse():
                        print(item)
            else:
                if arg == "pre":
                    if isinstance(
                        self._tree,
                        threaded_binary_tree.RightThreadedBinaryTree
                    ) or isinstance(
                        self._tree,
                        threaded_binary_tree.DoubleThreadedBinaryTree
                    ):
                        for item in self._tree.preorder_traverse():
                            print(item)
                    else:
                        for item in traversal.preorder_traverse(
                            tree=self._tree
                        ):
                            print(item)
                elif arg == "in":
                    if isinstance(
                        self._tree,
                        threaded_binary_tree.RightThreadedBinaryTree
                    ) or isinstance(
                        self._tree,
                        threaded_binary_tree.DoubleThreadedBinaryTree
                    ):
                        for item in self._tree.inorder_traverse():
                            print(item)
                    else:
                        for item in traversal.inorder_traverse(
                            tree=self._tree
                        ):
                            print(item)
                elif arg == "post":
                    for item in traversal.postorder_traverse(tree=self._tree):
                        print(item)
                elif arg == "rev-in":
                    if isinstance(
                        self._tree,
                        threaded_binary_tree.LeftThreadedBinaryTree
                    ) or isinstance(
                        self._tree,
                        threaded_binary_tree.DoubleThreadedBinaryTree
                    ):
                        for item in self._tree.reverse_inorder_traverse():
                            print(item)
                    else:
                        for item in traversal.reverse_inorder_traverse(
                            tree=self._tree
                        ):
                            print(item)
                else:
                    print(f"{arg} is an invalid traversal type")
        except KeyError as error:
            print(error)

    def do_detail(self, line):
        """Show the detail of the tree."""
        print(self._tree)

    def do_destroy(self, line):
        """Destroy the existing tree."""
        self._tree = None
        print("The tree has been destroyed.")

    def do_exit(self, line):
        """Exit the application."""
        print("Bye")
        raise SystemExit()

    def _get_single_arg(self, line):
        arg = line.split()
        if len(arg) > 1:
            raise KeyError("Too many arguments")
        else:
            return arg

    def _get_key(self, line):
        key = self._get_single_arg(line=line)

        if key[0].isdigit() is False:
            raise KeyError("The key must be an integer")
        else:
            return int(key[0])


def main():
    """Entry point for the tree CLI."""
    cli().cmdloop()
