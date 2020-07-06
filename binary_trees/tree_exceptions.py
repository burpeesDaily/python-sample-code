# Copyright © 2020 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Binary Tree Exception Definitions."""


class DuplicateKeyError(Exception):
    """Raised when a key already exists."""

    def __init__(self, key):
        Exception.__init__(self, f"{key} already exists.")


class KeyNotFoundError(Exception):
    """Raised when a key does not exist."""

    def __init__(self, key):
        Exception.__init__(self, f"{key} does not exist.")
