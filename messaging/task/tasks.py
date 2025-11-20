from celery import Celery
from messaging.config import Config
from messaging.db.conn import LocalSession
from messaging.db.message import Message

celery_app = Celery(
    'worker',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)


@celery_app.task(name='process_message')
def process_message(message_id):
    session = LocalSession()

    try:
        msg = session.get(Message, message_id)
        if not msg:
            print(f'No message found: {message_id}')
            return

        # Only for testing. Make pending status visible
        import time
        import random
        delay_seconds = random.randint(1, 10)
        print(f'Processing message {message_id} (delay: {delay_seconds}s)')
        time.sleep(delay_seconds)

        msg.status = 'completed'
        msg.result = {
            'processed': True,
            'delay': delay_seconds
        }
        session.commit()

        print(f'Completed message {message_id}')
        return msg.id

    finally:
        session.close()
