# Copyright © 2020 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Entry point for the Tree CLI application."""

from trees.bin import tree_cli

if __name__ == "__main__":
    tree_cli.cli().cmdloop()
