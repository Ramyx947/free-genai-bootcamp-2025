from flask import Blueprint, jsonify, request

from ..services.openai_service import generate_vocabulary
from ..utils.middleware import handle_errors

vocabulary_bp = Blueprint("vocabulary", __name__)


@vocabulary_bp.route("/generate", methods=["POST"])
@handle_errors
async def generate_vocab():
    """Generate vocabulary using OpenAI."""
    data = request.get_json()
    prompt = data.get("prompt") if data else None
    result = await generate_vocabulary(prompt=prompt)
    return jsonify(result)
