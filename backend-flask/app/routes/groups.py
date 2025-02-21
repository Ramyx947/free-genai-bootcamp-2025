from flask import Blueprint, jsonify, request
import sqlite3
from ..config import Config
from ..middleware import handle_errors

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/', methods=['GET'])
@handle_errors
def get_groups():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, name, description, word_count 
            FROM groups
        """)
        groups = cursor.fetchall()
        
        groups_list = [{
            'id': group[0],
            'name': group[1],
            'description': group[2],
            'wordCount': group[3]
        } for group in groups]
        
        return jsonify({
            'success': True,
            'data': groups_list
        })
    
    except Exception as e:
        raise e
    finally:
        conn.close()

@groups_bp.route('/', methods=['POST'])
def create_group():
    data = request.get_json()
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO groups (name, description, word_count)
            VALUES (?, ?, 0)
        """, (data['name'], data.get('description', '')))
        
        group_id = cursor.lastrowid
        conn.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'id': group_id,
                'name': data['name'],
                'description': data.get('description', ''),
                'wordCount': 0
            }
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        conn.close()
