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

        return jsonify(result)

    except ValueError as e:
        current_app.logger.error(f"Validation error in generate_vocab: {e}")
        # In testing mode, return the full error message; otherwise, a generic one.
        if current_app.config.get("TESTING") or current_app.config.get("DEBUG"):
            return jsonify({"error": str(e)}), 400
        else:
            return jsonify({"error": "Invalid input provided."}), 400
    except Exception as e:
        current_app.logger.error(f"Error in generate_vocab: {e}")
        return jsonify({"error": "An internal error occurred."}), 500


@vocabulary_bp.route("/", methods=["POST"])
@handle_errors
def create_vocabulary():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No JSON data provided")

        prompt = data.get("prompt")
        if not prompt:
            raise ValueError("Prompt is required")

        # ... rest of the function logic ...

    except ValueError as e:
        current_app.logger.error(f"Validation error in create_vocabulary: {e}")
        return jsonify({"error": "Invalid input provided."}), 400
    except Exception as e:
        current_app.logger.error(f"Unexpected error in create_vocabulary: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500
