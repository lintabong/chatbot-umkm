from flask import Blueprint, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from app import mongo, client, genai_context
from app.utils import date_utils
from app.extensions import create_chat
from google.genai import types

bp = Blueprint('chat', __name__, url_prefix='/chat')

user_id = ObjectId('6864ae06a2ec687a4fae7c0b')

@bp.post('')
def start_chat_route():
    new_chat_id = ObjectId()
    data = request.get_json()

    first_message = (data.get('message') or '').strip()

    doc = {
        '_id': new_chat_id,
        'userId': user_id,
        'createdAt': date_utils.now(),
        'updatedAt': None,
        'isDeleted': False,
        'createdAtAsEpoch': date_utils.now_timestamp(),
        'title': '',
        'messages': []
    }

    if first_message:
        chat = create_chat()

        response = chat.send_message(first_message)
            
        doc['messages'].append({
            'role': 'user',
            'content': first_message,
            'timestamp': date_utils.now_timestamp()
        })

        doc['messages'].append({
            'role': 'model',
            'content': response.text,
            'timestamp': date_utils.now_timestamp() + 1
        })

    mongo['genai_chat'].insert_one(doc)
    return jsonify({'chat_id': str(new_chat_id), 'content': response.text}), 201

@bp.get('/<chat_id>')
def get_chat_route(chat_id):
    try:
        chat = mongo['genai_chat'].find_one({'_id': ObjectId(chat_id)})

        if not chat:
            return jsonify({'error': 'Chat not found'}), 404
        chat['_id'] = str(chat['_id'])
        chat['userId'] = str(chat['userId'])
        return jsonify(chat), 200
    except InvalidId:
        return jsonify({"error": "Invalid ID"}), 400


@bp.post('/<chat_id>')
def send_chat(chat_id):
    data = request.get_json()

    mongo['genai_chat'].update_one(
            {'_id': ObjectId(chat_id)},
            {'$push': {'messages': {
                'role': 'user',
                'content': data['message'],
                'timestamp': date_utils.now_timestamp()
            }}}
        )

    result = mongo['genai_chat'].find_one({'_id': ObjectId(chat_id)})
    history = []

    if result:
        for message in result['messages']:
            row = types.Content(role=message['role'], parts=[types.Part.from_text(text=message['content'])])
            history.append(row)

    chat = create_chat(history)

    response = chat.send_message(data['message'])

    mongo['genai_chat'].update_one(
            {'_id': ObjectId(chat_id)},
            {'$push': {'messages': {
                'role': 'model',
                'content': response.text,
                'timestamp': date_utils.now_timestamp()
            }}}
        )

    return jsonify({'chat_id': chat_id, 'content': response.text}), 200
