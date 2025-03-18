import functools
import logging

from flask import current_app, jsonify, request

from .langchain_guardrails import LangChainRomanianGuardrails

logger = logging.getLogger(__name__)


def handle_errors(f):
    """Decorator to handle errors in routes without exposing sensitive information in production."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Log the full exception details internally
            logger.error(f"Error in {f.__name__}: {e}", exc_info=True)
            # If in testing or debug mode, return the detailed error; otherwise, return a generic error message
            if current_app.config.get("TESTING") or current_app.config.get("DEBUG"):
                error_message = str(e)
            else:
                error_message = "An internal server error occurred."
            return jsonify({"error": error_message}), 500

    return decorated_function


def apply_guardrails(f):
    """Apply LangChain guardrails to the request and response without leaking internal error details in production."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip guardrails if disabled in config
        if not current_app.config.get("GUARDRAILS_ENABLED", True):
            return f(*args, **kwargs)

        try:
            # Get request data
            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON data provided."}), 400

            # Extract text and formality preference
            text = data.get("text", "")
            formal = data.get("formal", True)

            # Apply input guardrails using LangChain
            guardrails = LangChainRomanianGuardrails()
            try:
                guardrails.validate_input(text)
            except ValueError as e:
                # In testing/debug mode, return the original validation error
                if current_app.config.get("TESTING") or current_app.config.get("DEBUG"):
                    error_message = str(e)
                else:
                    error_message = "Invalid input provided."
                return jsonify({"error": error_message}), 400

            # Call the original function
            response = f(*args, **kwargs)

            # If response is a tuple (response object, status code)
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
            # For other ValueErrors, treat similarly as above
            if current_app.config.get("TESTING") or current_app.config.get("DEBUG"):
                error_message = str(e)
            else:
                error_message = "Invalid input provided."
            return jsonify({"error": error_message}), 400
        except Exception as e:
            logger.error(f"Error in guardrails: {e}", exc_info=True)
            if current_app.config.get("TESTING") or current_app.config.get("DEBUG"):
                error_message = str(e)
            else:
                error_message = "Internal server error."
            return jsonify({"error": error_message}), 500

    return decorated_function
