import logging
import functools
from flask import request, jsonify, current_app
from .langchain_guardrails import LangChainRomanianGuardrails

logger = logging.getLogger(__name__)


def handle_errors(f):
    """Decorator to handle errors in routes."""

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({"error": str(e)}), 500

    return decorated_function


def apply_guardrails(f):
    """Apply LangChain guardrails to the request and response."""

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip guardrails if disabled in config
        if not current_app.config.get("GUARDRAILS_ENABLED", True):
            return f(*args, **kwargs)

        try:
            # Get request data
            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON data provided"}), 400

            # Extract text and formality preference
            text = data.get("text", "")
            formal = data.get("formal", True)

            # Apply input guardrails using LangChain
            guardrails = LangChainRomanianGuardrails()
            try:
                guardrails.validate_input(text)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            # Call the original function
            response = f(*args, **kwargs)

            # If response is a tuple (response, status_code)
            if isinstance(response, tuple) and len(response) == 2:
                resp_obj, status_code = response

                # Only process successful responses
                if status_code == 200:
                    # Get the response data
                    resp_data = resp_obj.get_json()
                    if resp_data and "response" in resp_data:
                        # Apply output guardrails using LangChain
                        resp_data["response"] = guardrails.process_output(
                            resp_data["response"], formal
                        )
                        return jsonify(resp_data), status_code
                return response

            return response

        except ValueError as e:
            # Handle validation errors
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error in guardrails: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    return decorated_function
