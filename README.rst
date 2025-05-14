Binary Tree Library
===================

.. image:: https://github.com/burpeesDaily/python-sample-code/actions/workflows/testing.yml/badge.svg
    :target: https://github.com/burpeesDaily/python-sample-code/actions/workflows/testing.yml

.. image:: https://github.com/burpeesDaily/python-sample-code/actions/workflows/linting.yml/badge.svg
    :target: https://github.com/burpeesDaily/python-sample-code/actions/workflows/linting.yml

.. image:: https://codecov.io/gh/burpeesDaily/python-sample-code/branch/main/graph/badge.svg?token=HC1BNJ7W8L 
    :target: https://codecov.io/gh/burpeesDaily/python-sample-code
    
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


The **Binary Tree Library** is an example for demonstrating how to use `Sphinx <https://www.sphinx-doc.org/>`_.

Although it is a sample project, the **Binary Tree Library** is a usable tree data structure library, and has the following tree data structures:

- AVL Tree
- Binary Search Tree

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

    git clone https://github.com/burpeesDaily/python-sample-code.git
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
        contacts["Matthew"] = "matthew@email.com"
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
