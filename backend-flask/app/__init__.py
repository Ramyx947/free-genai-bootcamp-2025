import datetime
import os

from flask import Flask, abort, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from .config import Config
from .extensions import db
from .swagger import swagger_config
from .utils.middleware import handle_errors


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

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
    from .routes import dashboard_bp, groups_bp, words_bp
    from .routes.vocabulary import vocabulary_bp

    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(words_bp, url_prefix="/api/words")
    app.register_blueprint(groups_bp, url_prefix="/api/groups")
    app.register_blueprint(vocabulary_bp, url_prefix="/api/vocabulary")

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
                    "message": "API is running",
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "version": "1.0.0",
                }
            )
        except Exception as e:
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

    @app.route("/api/docs/<api_endpoint>")
    @handle_errors
    def api_docs(api_endpoint):
        endpoint_data = {
            "dashboard": {
                "title": "Dashboard API",
                "method": "GET",
                "path": "/api/dashboard",
                "description": "Get learning statistics and progress information",
                "frontend_usage": "Dashboard component",
                "swagger_tag": "Dashboard/get_dashboard",
                "example_request": "GET /api/dashboard",
                "example_response": """{
    "stats": {
        "total_words": 100,
        "learned_words": 25,
        "active_groups": 5
    }
}""",
            },
            "words": {
                "title": "Words API",
                "method": "GET",
                "path": "/api/words",
                "description": "Get all vocabulary words",
                "frontend_usage": "WordList, StudyComponents",
                "swagger_tag": "Words/get_words",
                "example_request": "GET /api/words",
                "example_response": """{
    "success": true,
    "data": [
        {
            "id": 1,
            "romanian": "bună",
            "english": "good",
            "pronunciation": "boo-nuh",
            "part_of_speech": "adjective"
        }
    ]
}""",
            },
            "groups": {
                "title": "Groups API",
                "method": "GET",
                "path": "/api/groups",
                "description": "Get all word groups",
                "frontend_usage": "GroupsTable component",
                "swagger_tag": "Groups/get_groups",
                "example_request": "GET /api/groups",
                "example_response": """{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Basic Phrases",
            "description": "Essential Romanian phrases",
            "wordCount": 10
        }
    ]
}""",
            },
            "health": {
                "title": "Health Check API",
                "method": "GET",
                "path": "/api/health",
                "description": "Check API health status",
                "frontend_usage": "System monitoring",
                "swagger_tag": "Health/get_health",
                "example_request": "GET /api/health",
                "example_response": """{
    "status": "healthy",
    "message": "API is running",
    "timestamp": "2024-02-21T12:00:00Z",
    "version": "1.0.0"
}""",
            },
        }

        if api_endpoint not in endpoint_data:
            abort(404)

        return render_template(
            "endpoint_docs.html", endpoint_data=endpoint_data[api_endpoint]
        )

    return app
