from typing import Any, Dict, Optional

from flask import Request


def validate_request_data(request: Request) -> Optional[Dict[str, Any]]:
    """Validate and return JSON data from request.

    Args:
        request: Flask request object

    Returns:
        Dict of validated data or None if invalid

    Raises:
        ValueError: If request has no JSON data
    """
    if not request.is_json:
        raise ValueError("Request must be JSON")

    data = request.get_json()
    if not data:
        return None

    return data
