from datetime import datetime
from typing import Optional, Any


def clean_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == "true"
    return None


def clean_string(value: Optional[str]) -> Optional[str]:
    """
    Replaces \n, \t and multiple spaces with one space. Removes \r.
    Returns None if string ends up being empty.
    """
    if not value:
        return None
    cleaned = value.strip().replace("\n", " ").replace("\r", "").replace("\t", " ")
    cleaned = " ".join(filter(None, cleaned.split()))
    return cleaned or None


def clean_number(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def clean_float(value: Any) -> Optional[float]:
    """Parses float values, handling potential type issues."""
    if value is not None:
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    return None


def clean_name(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    # Remove extra spaces, standardize separators
    name = " ".join(name.split())
    # Additional name-specific cleaning...
    return name


def clean_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.rstrip("Z"))
    except ValueError:
        return None


def clean_geolocation(geolocation: str, swap_lat_lon: bool) -> Optional[list]:
    """
    Parse geolocation string and return as [lon, lat] array.
    Returns None if coordinates are invalid.
    Cordis geolocations with (brackets) are swapped.
    """
    if not geolocation:
        return None

    cleaned = geolocation.replace("(", "").replace(")", "")
    try:
        lat, lon = map(lambda x: float(x.strip()), cleaned.split(","))
        if swap_lat_lon and not geolocation.startswith("("):
            lat, lon = lon, lat
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            return None

        return [lat, lon]
    except (ValueError, TypeError):
        return None
