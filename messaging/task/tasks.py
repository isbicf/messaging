from datetime import datetime, UTC

from messaging.task.worker import worker
from messaging.db.conn import SessionLocal
from messaging.db.message import Message


@worker.task(name='process_message')
def process_message(message_id: int):
    session = SessionLocal()

    try:
        # Fetch the record
        msg = session.get(Message, message_id)
        if not msg:
            return {'error': f'Message {message_id} not found'}

        # Simulate processing work
        processed_value = f'Processed at {datetime.now(UTC).isoformat()}'

        # Update message
        msg.status = 'completed'
        msg.result = processed_value
        msg.updated_at = datetime.now(UTC)

        session.commit()

        return {
            'id': msg.id,
            'status': msg.status,
            'result': msg.result
        }

    except Exception as e:
        session.rollback()

        # Try to mark the message as failed
        msg = session.get(Message, message_id)
        if msg:
            msg.status = 'failed'
            msg.result = str(e)
            msg.updated_at = datetime.now(UTC)
            session.commit()

        return {'error': str(e)}

    finally:
        session.close()
