#!/usr/bin/env python3
"""
Utility functions.
"""
from typing import Mapping, Sequence, Any, Union, TypeVar

KT = TypeVar('KT')  # Key type
VT = TypeVar('VT')  # Value type

def access_nested_map(nested_map: Mapping[KT, Any], path: Sequence[KT]) -> Union[Any, None]:
    """
    Access a value in a nested dictionary-like structure using a sequence of keys.

    Args:
        nested_map (Mapping): The nested dictionary or map.
        path (Sequence): A sequence (e.g., tuple) of keys representing the path
                         to the desired value.

    Returns:
        Any: The value found at the end of the path.
        Raises KeyError if any key in the path is not found.
    """
    current_value = nested_map
    for key in path:
        if not isinstance(current_value, Mapping):
            raise TypeError(f"Value at path before key '{key}' is not a mapping.")
        if key not in current_value:
            raise KeyError(key)
        current_value = current_value[key]
    return current_value

if __name__ == '__main__':
    # Example usage (as mentioned in "Play with it in the Python console")
    print(access_nested_map({"a": 1}, ("a",)))  # Expected: 1
    print(access_nested_map({"a": {"b": 2}}, ("a",)))  # Expected: {"b": 2}
    print(access_nested_map({"a": {"b": 2}}, ("a", "b")))  # Expected: 2

    try:
        print(access_nested_map({"a": {"b": 2}}, ("a", "c")))
    except KeyError as e:
        print(f"KeyError caught as expected: {e}")

    try:
        print(access_nested_map({"a": 1}, ("a", "b")))
    except TypeError as e:
        print(f"TypeError caught as expected: {e}")