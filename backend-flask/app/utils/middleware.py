import logging
from functools import wraps
from typing import Any, Dict, Tuple

from flask import jsonify, request

logger = logging.getLogger(__name__)


def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs) -> Tuple[Dict[str, Any], int]:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Log the error with context
            logger.error(f"Error: {str(e)}")
            logger.error(f"Function: {f.__name__}")
            logger.error(f"Path: {request.path}")
            logger.error(f"Method: {request.method}")

            # Return standardized error response
            return (
                jsonify(
                    {
                        "success": False,
                        "error": str(e),
                        "path": request.path,
                        "method": request.method,
                    }
                ),
                500,
            )

    return wrapper
