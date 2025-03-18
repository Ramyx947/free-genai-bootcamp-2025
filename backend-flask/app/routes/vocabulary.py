from asgiref.sync import async_to_sync
from flask import Blueprint, current_app, jsonify, request

from ..services.openai_service import generate_vocabulary
from ..utils.langchain_guardrails import LangChainRomanianGuardrails
from ..utils.middleware import handle_errors

vocabulary_bp = Blueprint("vocabulary", __name__)


@vocabulary_bp.route("/generate", methods=["POST"])
@handle_errors
def generate_vocab():
    """Generate vocabulary using OpenAI with LangChain guardrails."""
    try:
        data = request.get_json()

        text = data.get("text")
        if not text:
            return jsonify({"error": "Text is required"}), 400

        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        formal = data.get("formal", True)

        # Apply input guardrails using LangChain
        guardrails = LangChainRomanianGuardrails()
        guardrails.validate_input(text)

        # Use async_to_sync to call the async function
        result = async_to_sync(generate_vocabulary)(prompt, formal)

        # Apply output guardrails using LangChain
        if "response" in result:
            result["response"] = guardrails.process_output(result["response"], formal)

        # Return the result
        return jsonify(result)

    except ValueError as e:
        # Handle validation errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error in generate_vocab: {str(e)}")
        return jsonify({"error": str(e)}), 500


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
