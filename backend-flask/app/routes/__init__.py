"""API route blueprints."""
from .dashboard import dashboard_bp
from .groups import groups_bp
from .vocabulary import vocabulary_bp
from .words import words_bp

# Export the blueprints
__all__ = ["dashboard_bp", "groups_bp", "vocabulary_bp", "words_bp"]
