from flask import jsonify

def handle_error(error_code, message, details=None):
    response = {
        "code": error_code,
        "message": message,
        "details": details or {}
    }
    return jsonify(response), 400