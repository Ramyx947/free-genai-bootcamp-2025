from functools import wraps
from flask import current_app, jsonify, request
import logging

logger = logging.getLogger(__name__)

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            logger.error(f"Request path: {request.path}")
            logger.error(f"Request method: {request.method}")
            logger.error(f"Request headers: {dict(request.headers)}")
            
            return jsonify({
                "error": "Internal server error",
                "message": str(e)
            }), 500
    return decorated_function 