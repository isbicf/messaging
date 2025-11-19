import traceback
from flask import Blueprint, request, jsonify
from messaging.db.conn import LocalSession
from messaging.service.message import MessageService
from messaging.task.tasks import process_message

message_bp = Blueprint('message_bp', __name__)


# POST /messages
@message_bp.route('', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON payload is required'}), 400

    session = LocalSession()
    service = MessageService(session)

    try:
        msg = service.create(data.get('payload', '{}'))     # Save message
        process_message.delay(msg.id)   # Enqueue background task
        return jsonify({'id': msg.id, 'status': msg.status}), 201
    except Exception as e:
        session.rollback()
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# GET /messages
@message_bp.route('', methods=['GET'])
def list_messages():
    status = request.args.get('status')
    session = LocalSession()
    service = MessageService(session)

    try:
        messages = service.list(status)
        result = [
            {
                'id': m.id,
                'payload': m.payload,
                'status': m.status,
                'result': m.result,
                'created_at': m.created_at.isoformat(),
                'updated_at': m.updated_at.isoformat(),
            }
            for m in messages
        ]
        return jsonify(result), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# GET /messages/<id>
@message_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    session = LocalSession()
    service = MessageService(session)

    try:
        msg = service.get(message_id)
        if not msg:
            return jsonify({'error': 'Message not found'}), 404

        return jsonify({
            'id': msg.id,
            'payload': msg.payload,
            'status': msg.status,
            'result': msg.result,
            'created_at': msg.created_at.isoformat(),
            'updated_at': msg.updated_at.isoformat(),
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# GET /messages/stats
@message_bp.route('/stats', methods=['GET'])
def get_stats():
    session = LocalSession()
    service = MessageService(session)

    try:
        stats = service.stats()
        return jsonify(stats), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
