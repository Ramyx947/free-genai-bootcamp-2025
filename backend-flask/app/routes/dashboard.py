from flask import Blueprint, jsonify
from ..middleware import handle_errors

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
@handle_errors
def get_dashboard():
    try:
        return jsonify({
            "stats": {
                "total_words": 100,
                "learned_words": 25,
                "active_groups": 5
            }
        })
    except Exception as e:
        raise e
