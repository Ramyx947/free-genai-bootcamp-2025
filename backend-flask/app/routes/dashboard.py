"""
Dashboard Routes

Provides statistics and overview of:
- Learning progress
- Word counts
- Study sessions
"""

from flask import Blueprint, jsonify

from ..models import Group, Word
from ..utils.middleware import handle_errors

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/", methods=["GET"])
@handle_errors
def get_dashboard():
    """Get dashboard overview.

    Returns:
        JSON with:
        - Last study session
        - Learning progress
        - Overall statistics
    """
    # Clear section comments
    # Last session info
    last_session = {"date": None, "score": 0, "duration": 0, "activity": None}

    # Progress tracking
    progress = {
        "totalWordsLearned": Word.query.filter(Word.learned.is_(True)).count(),
        "completionRate": 0,
        "streak": 0,
    }

    # Overall statistics
    stats = {
        "totalWords": Word.query.count(),
        "totalGroups": Group.query.count(),
        "completedSessions": 0,
    }

    return jsonify(
        {
            "success": True,
            "data": {"lastSession": last_session, "progress": progress, "stats": stats},
        }
    )
