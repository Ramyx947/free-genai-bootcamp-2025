from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import Group
from ..utils.middleware import handle_errors

groups_bp = Blueprint("groups", __name__)


@groups_bp.route("/", methods=["GET"])
@handle_errors
def get_groups():
    """Get all groups."""
    groups = Group.query.all()
    return jsonify({"success": True, "data": [group.to_dict() for group in groups]})


@groups_bp.route("/", methods=["POST"])
@handle_errors
def create_group():
    """Create a new group using SQLAlchemy."""
    data = request.get_json()
    group = Group(
        name=data["name"], description=data.get("description", ""), word_count=0
    )
    db.session.add(group)
    db.session.commit()

    return jsonify({"success": True, "data": group.to_dict()}), 201
