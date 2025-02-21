from flask import Blueprint, jsonify

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
def get_dashboard():
    return jsonify({
        "message": "Dashboard endpoint",
        "data": {
            "total_words": 0,
            "learned_words": 0
        }
    }), 200
