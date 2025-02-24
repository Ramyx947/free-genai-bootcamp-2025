from typing import Any, Dict, Optional

from flask import jsonify


def api_response(
    data: Optional[Any] = None, message: Optional[str] = None, status_code: int = 200
) -> tuple:
    """Standardize API responses."""
    response: Dict = {"success": 200 <= status_code < 300}

    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message

    return jsonify(response), status_code
