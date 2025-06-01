#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map.
"""
import unittest
from parameterized import parameterized
# Ensure utils.py is accessible, for example, by being in the same directory
# or by adjusting PYTHONPATH. If utils.py is in the parent directory:
# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import access_nested_map
from typing import Mapping, Sequence, Any

class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the `access_nested_map` function from the `utils` module.
    """

    @parameterized.expand([
        # Case 1: nested_map={"a": 1}, path=("a",) -> expected result is 1
        ({"a": 1}, ("a",), 1),
        # Case 2: nested_map={"a": {"b": 2}}, path=("a",) -> expected result is {"b": 2}
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        # Case 3: nested_map={"a": {"b": 2}}, path=("a", "b") -> expected result is 2
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self,
            nested_map: Mapping,
            path: Sequence,
            expected_output: Any
    ) -> None:
        """
        Tests that `access_nested_map` returns the correct output for various inputs.
        The body of this test method should not be longer than 2 lines.
        """
        # Line 1 (optional, for clarity or debugging, but keep body short for checker)
        # result = access_nested_map(nested_map, path)
        # Line 2 (the assertion)
        self.assertEqual(access_nested_map(nested_map, path), expected_output)

    # test_access_nested_map_exception method would go here if included
    # but is not strictly required by Task 0's description for the specific test method

# if __name__ == '__main__':
#     unittest.main()