"""API route blueprints."""

from flask import Flask


def register_blueprints(app: Flask):
    """Register all blueprints with the app."""
    from .dashboard import dashboard_bp
    from .groups import groups_bp
    from .vocabulary import vocabulary_bp
    from .words import words_bp

    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(words_bp, url_prefix="/api/words")
    app.register_blueprint(groups_bp, url_prefix="/api/groups")
    app.register_blueprint(vocabulary_bp, url_prefix="/api/vocabulary")


# Export the blueprints
__all__ = ["dashboard_bp", "groups_bp", "vocabulary_bp", "words_bp"]
