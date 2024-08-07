import json
import os
from pathlib import Path
from typing import List, Dict, Any, Callable

from utils.error_handling.error_handling import log_and_raise_exception


def get_all_keys_value_recursively(file_path: Path, key: str) -> List[Any]:
    """
    Searches all JSON files in all subdirectories under the file_path for the specified key.
    Returns a list of all values for all matching keys.
    """
    return _process_json_files(file_path, lambda fp: extract_key_values(fp, key))


def get_all_keys_as_dict_recursively(file_path: Path, key: str) -> List[Dict[str, Any]]:
    """
    Searches all JSON files in all subdirectories under the file_path for the specified key.
    Returns a list of dictionaries for all matching keys.
    """
    return _process_json_files(file_path, lambda fp: extract_object(fp, key))


def _process_json_files(file_path: Path, extraction_func: Callable) -> List[Any]:
    """
    Walks through all JSON files in the given file_path and applies the extraction_func to each.
    """
    all_values = []
    for root, _, files in os.walk(file_path):
        for file in files:
            if file.endswith(".json"):
                full_file_path = os.path.join(root, file)
                values = extraction_func(full_file_path)
                all_values.extend(values)
    return all_values


def extract_key_values(file_path: Path, key: str) -> List[Any]:
    """
    Extracts the value of the specified key from a JSON file.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return _find_key_values(data, key)
    except json.JSONDecodeError:
        print(f"Error parsing JSON file: {file_path}")
        return []


def extract_object(file_path: Path, key: str) -> List[Dict[str, Any]]:
    """
    Extracts the object with the specified key from a JSON file.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return _find_key_objects(data, key)
    except json.JSONDecodeError:
        log_and_raise_exception(f"Error parsing JSON file: {file_path}")


def _find_key_values(obj: Any, key: str) -> List[Any]:
    """
    Recursively searches for all values of the specified key in a JSON object.
    """
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                results.append(v)
            results.extend(_find_key_values(v, key))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(_find_key_values(item, key))
    return results


def _find_key_objects(obj: Any, key: str) -> List[Dict[str, Any]]:
    """
    Recursively searches for all objects containing the specified key in a JSON object.
    """
    results = []
    if isinstance(obj, dict):
        if key in obj:
            results.append(obj)
        for v in obj.values():
            results.extend(_find_key_objects(v, key))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(_find_key_objects(item, key))
    return results


if __name__ == "__main__":
    json_path = Path(
        "/Users/wehrenberger/Code/DIGICHer/DIGICHer_Pipeline/data/pile/extractors/core_culturalANDheritage/last_publishedDate_None"
    )

    # Example to find all values with the same key in all files
    published_dates = get_all_keys_value_recursively(json_path, "publishedDate")
    print(f"{len(published_dates)}, {min(published_dates)}, {max(published_dates)}")

    # Example to find all objects containing a specific key in all files
    # link_objects = get_all_objects(json_path, "url")
    # print("Link objects:", link_objects)
