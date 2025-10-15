"""
Tool: Data Merging Operations
Category: aggregation
Description: Functions for merging and combining data from multiple sources
"""

from typing import List, Dict, Any


def merge_by_key(
    data1: List[Dict[str, Any]],
    data2: List[Dict[str, Any]],
    key_field: str,
    merge_strategy: str = "left"
) -> List[Dict[str, Any]]:
    """Merge two datasets based on a common key field.


    Args:
        data1: First dataset (list of dictionaries)
        data2: Second dataset (list of dictionaries)
        key_field: Field name to use as merge key
        merge_strategy: "left", "right", "inner", or "outer"

    Returns:
        Merged dataset

    Example:
        doors = [{"element_id": "D1", "width": 900}, {"element_id": "D2", "width": 800}]
        fire_ratings = [{"element_id": "D1", "fire_rating": "FD30"}]
        merged = merge_by_key(doors, fire_ratings, "element_id", "left")
        # Returns: [
        #     {"element_id": "D1", "width": 900, "fire_rating": "FD30"},
        #     {"element_id": "D2", "width": 800}
        # ]
    """
    # Create lookup dictionary for data2
    lookup = {item[key_field]: item for item in data2 if key_field in item}

    result = []

    if merge_strategy in ["left", "outer"]:
        for item1 in data1:
            merged_item = item1.copy()
            key = item1.get(key_field)
            if key and key in lookup:
                # Merge data2 fields into item1
                for k, v in lookup[key].items():
                    if k != key_field:  # Don't duplicate the key field
                        merged_item[k] = v
            result.append(merged_item)

    if merge_strategy in ["right", "outer"]:
        # Add items from data2 that weren't in data1
        keys_in_data1 = {item.get(key_field) for item in data1}
        for item2 in data2:
            key = item2.get(key_field)
            if key and key not in keys_in_data1:
                result.append(item2.copy())

    if merge_strategy == "inner":
        for item1 in data1:
            key = item1.get(key_field)
            if key and key in lookup:
                merged_item = item1.copy()
                for k, v in lookup[key].items():
                    if k != key_field:
                        merged_item[k] = v
                result.append(merged_item)

    return result


def combine_lists(*data_lists: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Combine multiple lists into a single list.


    Args:
        *data_lists: Variable number of data lists to combine

    Returns:
        Combined list

    Example:
        doors_l1 = [{"element_id": "D1", "floor": "L1"}]
        doors_l2 = [{"element_id": "D2", "floor": "L2"}]
        all_doors = combine_lists(doors_l1, doors_l2)
        # Returns: [{"element_id": "D1", "floor": "L1"}, {"element_id": "D2", "floor": "L2"}]
    """
    result = []
    for data_list in data_lists:
        result.extend(data_list)
    return result


def flatten_grouped_data(grouped_data: Dict[Any, List[Dict[str, Any]]], group_key_name: str = "group") -> List[Dict[str, Any]]:
    """Flatten grouped data back into a single list, adding group key as a field.


    Args:
        grouped_data: Dictionary of grouped elements
        group_key_name: Name to use for the group key field in output

    Returns:
        Flattened list with group keys added

    Example:
        grouped = {
            "Level 1": [{"element_id": "D1"}, {"element_id": "D2"}],
            "Level 2": [{"element_id": "D3"}]
        }
        flattened = flatten_grouped_data(grouped, "floor")
        # Returns: [
        #     {"element_id": "D1", "floor": "Level 1"},
        #     {"element_id": "D2", "floor": "Level 1"},
        #     {"element_id": "D3", "floor": "Level 2"}
        # ]
    """
    result = []
    for group_key, items in grouped_data.items():
        for item in items:
            new_item = item.copy()
            new_item[group_key_name] = group_key
            result.append(new_item)
    return result


def deduplicate_by_key(data: List[Dict[str, Any]], key_field: str, keep: str = "first") -> List[Dict[str, Any]]:
    """Remove duplicate entries based on a key field.


    Args:
        data: List of dictionaries
        key_field: Field name to use for identifying duplicates
        keep: "first" or "last" - which duplicate to keep

    Returns:
        List with duplicates removed

    Example:
        data = [
            {"element_id": "D1", "version": 1},
            {"element_id": "D1", "version": 2},
            {"element_id": "D2", "version": 1}
        ]
        unique = deduplicate_by_key(data, "element_id", "last")
        # Returns: [
        #     {"element_id": "D1", "version": 2},
        #     {"element_id": "D2", "version": 1}
        # ]
    """
    seen = {}

    if keep == "first":
        for item in data:
            key = item.get(key_field)
            if key and key not in seen:
                seen[key] = item
    else:  # keep == "last"
        for item in data:
            key = item.get(key_field)
            if key:
                seen[key] = item

    return list(seen.values())
