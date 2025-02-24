from flask import Blueprint, jsonify

from ..models import Word
from ..utils.middleware import handle_errors

words_bp = Blueprint("words", __name__)


@words_bp.route("/", methods=["GET"])
@handle_errors
def get_words():
    """Get all words."""
    words = Word.query.all()
    return jsonify({"success": True, "data": [word.to_dict() for word in words]})


@words_bp.route("/<int:word_id>", methods=["GET"])
@handle_errors
def get_word(word_id):
    # Your route logic here
    return jsonify({"id": word_id, "word": "casă", "translation": "house"})
