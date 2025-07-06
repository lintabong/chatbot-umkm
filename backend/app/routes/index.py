from flask import Blueprint, jsonify

bp = Blueprint('index', __name__, url_prefix='')

@bp.get('/')
def index():
    return jsonify({
        'title': 'Chatbot Gemini AI for UMKM'
    }), 200
