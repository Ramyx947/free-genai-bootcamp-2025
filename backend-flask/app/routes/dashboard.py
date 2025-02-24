from flask import Blueprint, jsonify

from ..utils.middleware import handle_errors
from ..models.word import Word
from ..models.group import Group

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/", methods=["GET"])
@handle_errors
def get_dashboard():
    """Get dashboard statistics.
    
    Returns:
        JSON: A dictionary containing:
            - message: Success message
            - data: Dictionary containing:
                - total_words: Total number of words in system
                - learned_words: Number of learned words
                - active_groups: Number of active groups
    """
    stats = {
        "total_words": Word.query.count(),
        "learned_words": Word.query.filter_by(learned=True).count(),
        "active_groups": Group.query.filter_by(active=True).count()
    }
    
    return jsonify({
        "message": "Dashboard data retrieved successfully",
        "data": stats
    })
