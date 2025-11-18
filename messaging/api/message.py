import traceback
from flask import Blueprint, request, jsonify
from messaging.db.conn import SessionLocal
from messaging.db.message import Message
from messaging.task.tasks import process_message

message_bp = Blueprint('message_bp', __name__)


# POST /messages  - create new message & enqueue Celery task
@message_bp.route('', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON payload is required'}), 400

    session = SessionLocal()

    try:
        # 1. Insert record
        msg = Message(
            payload=data.get('payload', '{}'),
            status='pending'
        )
        session.add(msg)
        session.commit()
        session.refresh(msg)

        # 2. Enqueue Celery background job
        process_message.delay(msg.id)

        return jsonify({'id': msg.id, 'status': msg.status}), 201

    except Exception as e:
        session.rollback()
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# GET /messages?status=pending
@message_bp.route('', methods=['GET'])
def list_messages():
    status = request.args.get('status')
    session = SessionLocal()

    try:
        query = session.query(Message)
        if status:
            query = query.filter(Message.status == status)

        messages = query.order_by(Message.created_at.desc()).all()

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
        session.rollback()
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# GET /messages/<id>
@message_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    session = SessionLocal()

    try:
        msg = session.get(Message, message_id)
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
        session.rollback()
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# GET /messages/stats
@message_bp.route('/stats', methods=['GET'])
def get_stats():
    session = SessionLocal()

    try:
        total = session.query(Message).count()
        pending = session.query(Message).filter(Message.status == 'pending').count()
        completed = session.query(Message).filter(Message.status == 'completed').count()
        failed = session.query(Message).filter(Message.status == 'failed').count()

        return jsonify({
            'total': total,
            'pending': pending,
            'completed': completed,
            'failed': failed
        }), 200
    except Exception as e:
        session.rollback()
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
