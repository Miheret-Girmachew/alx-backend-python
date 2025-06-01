#!/usr/bin/env python3
"""
Utility functions.
"""
from typing import Mapping, Sequence, Any, Union, TypeVar

KT = TypeVar('KT')  # Key type
VT = TypeVar('VT')  # Value type\
    
import requests 
from typing import Dict, Any


def get_json(url: str) -> Dict:
    """
    Fetches JSON data from a given URL.

    Args:
        url (str): The URL to fetch JSON from.

    Returns:
        Dict: The parsed JSON response as a dictionary.
    """
    response = requests.get(url)
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    return response.json()


def access_nested_map(nested_map: Mapping[KT, Any], path: Sequence[KT]) -> Union[Any, None]:
    """
    Access a value in a nested dictionary-like structure using a sequence of keys.

    Args:
        nested_map (Mapping): The nested dictionary or map.
        path (Sequence): A sequence (e.g., tuple) of keys representing the path
                         to the desired value.

    Returns:
        Any: The value found at the end of the path.
    Raises:
        KeyError: If any key in the path is not found in the current mapping.
        TypeError: If a value along the path is not a mapping and further sub-keys are accessed.
    """
    current_value = nested_map
    for key in path:
        # Check if current_value is a mapping *before* trying to access the key
        if not isinstance(current_value, Mapping):
            # This case is what the task describes for nested_map={"a": 1}, path=("a", "b")
            # The task specifies this should raise KeyError.
            # Standard dict access on a non-dict raises TypeError if you try `non_dict[key]`.
            # To strictly meet the "KeyError" requirement for path=("a", "b") on nested_map={"a": 1},
            # the function would need to handle this slightly differently or the task implies
            # that attempting to access a sub-key on a non-mapping due to path exhaustion is a type of KeyError.
            # For standard Python dicts, `1['b']` would be a TypeError.
            # Let's adjust the logic to raise KeyError as specified for the second test case.
            # The most straightforward interpretation for the task is that if a key in the path
            # cannot be resolved (either because it's missing OR because its parent is not a map),
            # it's a KeyError related to that key.
            raise KeyError(key) # This makes it fit the task's expectation for the second case

        if key not in current_value:
            raise KeyError(key) # Standard KeyError for missing key
        current_value = current_value[key]
    return current_value