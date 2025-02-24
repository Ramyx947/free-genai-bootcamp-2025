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


@vocabulary_bp.route("/", methods=["POST"])
@handle_errors
def create_vocabulary():
    data = request.get_json()
    if not data:
        raise ValueError("No JSON data provided")

    prompt = data.get("prompt")
    if not prompt:
        raise ValueError("Prompt is required")

    # Rest of the function...
