from flask import Blueprint, jsonify
import sqlite3
from ..config import Config
from ..middleware import handle_errors

words_bp = Blueprint('words', __name__)

@words_bp.route('/', methods=['GET'])
@handle_errors
def get_words():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get all words with their details
        cursor.execute("""
            SELECT id, romanian, english, pronunciation, part_of_speech, parts 
            FROM words
        """)
        words = cursor.fetchall()
        
        # Convert to list of dictionaries
        words_list = [{
            'id': word[0],
            'romanian': word[1],
            'english': word[2],
            'pronunciation': word[3],
            'part_of_speech': word[4],
            'parts': word[5]
        } for word in words]
        
        return jsonify({
            'success': True,
            'data': words_list
        })
    
    except Exception as e:
        raise e
    
    finally:
        conn.close()

@words_bp.route('/<int:word_id>', methods=['GET'])
@handle_errors
def get_word(word_id):
    try:
        # Your route logic here
        return jsonify({
            "id": word_id,
            "word": "casă",
            "translation": "house"
        })
    except Exception as e:
        raise e
