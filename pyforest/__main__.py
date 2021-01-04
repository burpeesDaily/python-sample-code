# Copyright © 2020 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Entry point for the Forest CLI application."""

from pyforest.bin import forest_cli

if __name__ == "__main__":
    forest_cli.cli().cmdloop()
