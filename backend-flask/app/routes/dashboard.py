from flask import Blueprint, jsonify

from ..utils.middleware import handle_errors

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/", methods=["GET"])
@handle_errors
def get_dashboard():
    return jsonify(
        {
            "message": "Dashboard data retrieved successfully",
            "data": {"total_words": 100, "learned_words": 25, "active_groups": 5},
        }
    )
