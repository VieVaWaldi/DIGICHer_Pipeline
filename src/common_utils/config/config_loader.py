import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

from core.etl.extractor.utils import clean_extractor_name
from core.file_handling.file_handling import get_root_path, load_json_file


def get_data_path(source_name: str, config: Dict, run: int):
    assert config, "config must be a non-empty dict"
    assert run >= 0

    path = Path(config["data_path"]) / (
        source_name
        + "_"
        + clean_extractor_name(get_query_config()[source_name]["runs"][run]["query"])
    )
    if os.getenv("ENV") == "dev":
        return get_root_path() / path
    return path


def get_config() -> Dict[str, Any]:
    """Returns default config as json"""
    return _get_config("config")


def get_query_config() -> Dict[str, Any]:
    """Returns query config as json"""
    return _get_config("config_queries")


def _get_config(config_name: str) -> Dict[str, Any]:
    """Prepares and returns the given config as json"""
    config_file_path = get_root_path() / "configs" / f"{config_name}.json"

    config = load_json_file(config_file_path)
    if not config:
        raise Exception("Error reading the logger file.")

    load_dotenv()
    env = os.getenv("ENV")
    if env not in config:
        return config
    return config[env]
