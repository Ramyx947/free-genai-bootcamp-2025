from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'romanian-learning'
    })

@health_bp.route('/health/detailed')
def detailed_health():
    """Detailed health check with component status"""
    return jsonify({
        'status': 'healthy',
        'components': {
            'audio_service': check_audio_service(),
            'question_service': check_question_service(),
            'transcript_service': check_transcript_service()
        },
        'timestamp': datetime.utcnow().isoformat()
    })

def check_audio_service():
    # Implement audio service health check
    return {'status': 'operational'}

def check_question_service():
    # Implement question service health check
    return {'status': 'operational'}

def check_transcript_service():
    # Implement transcript service health check
    return {'status': 'operational'} 