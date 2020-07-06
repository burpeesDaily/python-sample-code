import cmd

from binary_trees import binary_search_tree
from binary_trees import traversal
from binary_trees import tree_exceptions


class cli(cmd.Cmd):
    intro = "Welcome to the simple CLI. Type help or ? to list commands.\n"
    prompt = "cli> "

    def __init__(self):
        cmd.Cmd.__init__(self)
        self._tree = binary_search_tree.BinarySearchTree()

    def _get_key(self, line):
        key = line.split()

        if key[0].isdigit() is False:
            raise KeyError("The key must be an integer")
        else:
            return int(key[0])

    def do_search(self, line):
        """Search data by a given key.

        Example:
        cli> search 3
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
        cli> insert 7 data
        """
        args = line.split()
        if len(args) != 2:
            print("Invalid number of the arguments")
        else:
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
        cli> delete 5
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

        Options: pre, in, post, level
        Example:
        cli> traverse level
        """
        arg = line.lower()
        if arg == "pre":
            for item in traversal.preorder_traverse(tree=self._tree):
                print(item)
        elif arg == "in":
            for item in traversal.inorder_traverse(tree=self._tree):
                print(item)
        elif arg == "post":
            for item in traversal.postorder_traverse(tree=self._tree):
                print(item)
        elif arg == "level":
            for item in traversal.levelorder_traverse(tree=self._tree):
                print(item)
        else:
            print(f"{arg} is an invalid traversal type")

    def do_exit(self, line):
        """Exit the application."""
        print("Bye")
        raise SystemExit()


if __name__ == "__main__":
    cli().cmdloop()
