import datetime
import os
import logging

from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .config import get_config
from .extensions import db
from .swagger import swagger_config
from .utils.middleware import handle_errors
from .routes import register_blueprints

# Add logger configuration
logger = logging.getLogger(__name__)

# Create extensions
migrate = Migrate()

# Create a limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    # Configure SQLAlchemy engine options based on environment
    if config_name == "testing":
        # No pooling for testing
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}
    else:
        # Use connection pooling for development/production
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_size": 10,
            "pool_recycle": 3600,
            "pool_pre_ping": True,
            "pool_timeout": 30,
        }

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # Update CORS configuration
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173",  # Vite dev server
                    "http://localhost:5000",  # Flask backend
                    "http://localhost",  # Production
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
            }
        },
    )

    # Disable strict slashes
    app.url_map.strict_slashes = False

    # Register Swagger UI blueprint with custom template
    SWAGGER_URL = "/api/docs"
    API_URL = "/static/swagger.json"

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Romanian Learning API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/docs")
    def swagger_ui():
        return render_template(
            "swagger_ui.html",
            title="Romanian Learning API Documentation",
            swagger_ui_css=(
                "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/"
                "4.15.5/swagger-ui.min.css"
            ),
            swagger_ui_bundle_js=(
                "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/"
                "4.15.5/swagger-ui-bundle.min.js"
            ),
            swagger_ui_standalone_preset_js=(
                "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/"
                "4.15.5/swagger-ui-standalone-preset.min.js"
            ),
            base_url=API_URL,
        )

    # Serve swagger spec
    @app.route("/static/swagger.json")
    def specs():
        return jsonify(swagger_config)

    # Register API blueprints
    register_blueprints(app)

    @app.route("/")
    @handle_errors
    def root():
        try:
            return render_template("api_docs.html")
        except Exception as e:
            raise e

    @app.route("/api/health")
    @handle_errors
    def health_check():
        try:
            return jsonify(
                {
                    "status": "healthy",
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                    "version": "1.0.0",
                }
            )
        except Exception as e:
            app.logger.error(f"Health check error: {str(e)}")
            raise e

    # Add favicon route
    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    # Add error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return (
            jsonify(
                {
                    "error": "Not Found",
                    "message": "The requested URL was not found on the server.",
                }
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {
                    "error": "Method Not Allowed",
                    "message": "The method is not allowed for the requested URL.",
                }
            ),
            405,
        )

    # Enable guardrails based on configuration
    if app.config.get("GUARDRAILS_ENABLED", True):
        logger.info("Guardrails enabled for Romanian language learning")

    # Configure for async support
    app.config["PROPAGATE_EXCEPTIONS"] = True

    return app
