Sample Binary Tree Library
##########################

.. image:: https://github.com/shunsvineyard/python-sample-code/workflows/Test/badge.svg
    :target: https://github.com/shunsvineyard/python-sample-code/actions?query=workflow%3ATest

.. image:: https://github.com/shunsvineyard/python-sample-code/workflows/Linting/badge.svg 
    :target: https://github.com/shunsvineyard/python-sample-code/actions?query=workflow%3ALinting

.. image:: https://codecov.io/gh/shunsvineyard/python-sample-code/branch/main/graph/badge.svg?token=zLkKU6p7do
    :target: https://codecov.io/gh/shunsvineyard/python-sample-code
    
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


The **Binary Tree Library** is a Python sample project used by shunsvineyard.info. It is an example for `Sphinx <https://www.sphinx-doc.org/>`_ and `My Python Coding Style <https://www.formosa1544.com/2019/01/05/my-python-coding-style-and-principles/>`_.

Although it is a sample project, the **Binary Tree Library** is a usable tree data structure library, and has the following tree data structures:

- AVL Tree
- Binary Search Tree
- Red Black Tree
- Threaded Binary Trees

The library also provides the tree traversal feature to traverse binary trees.

- Binary Tree Traversal
    - In-order
    - Reversed In-order
    - Pre-order
    - Post-order
    - Level-order

Requirements
------------

The **Binary Tree Library** requires Python 3.9 or newer.

Installation
------------

Install from Github

.. code-block:: text

    git clone https://github.com/shunsvineyard/python-sample-code.git
    cd python-sample-code
    pip install .

Examples
--------

.. code-block:: python

    from trees import tree_exceptions
    from trees.binary_trees import red_black_tree
    from trees.binary_trees import traversal


    class Map:
        def __init__(self):
            self._rbt = red_black_tree.RBTree()

        def __setitem__(self, key, value):
            self._rbt.insert(key=key, data=value)

        def __getitem__(self, key):
            return self._rbt.search(key=key).data

        def __delitem__(self, key):
            self._rbt.delete(key=key)

        def __iter__(self):
            return traversal.inorder_traverse(tree=self._rbt)


    if __name__ == "__main__":

        # Initialize the Map instance.
        contacts = Map()

        # Add some items.
        contacts["Mark"] = "mark@email.com"
        contacts["John"] = "john@email.com"
        contacts["Luke"] = "luke@email.com"
        contacts["john"] = "john@email.com"

        # Iterate the items.
        for contact in contacts:
            print(contact)

        # Delete one item.
        del contacts["john"]

        # Check the deleted item.
        try:
            print(contacts["john"])
        except tree_exceptions.KeyNotFoundError:
            print("john does not exist")


Tree CLI
--------

The **Binary Tree Library** provides a command line tool to simulate tree data structures.

.. code-block:: text

    tree-cli

It will show the interactive prompt. Use ``help`` to list all the available commands


.. code-block:: text

    Welcome to the Tree CLI. Type help or ? to list commands.

    tree> help

    Documented commands (type help <topic>):
    ========================================
    build  delete  destroy  detail  exit  help  insert  search  traverse
