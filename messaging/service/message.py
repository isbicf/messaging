from messaging.db.message import Message


class MessageService:
    def __init__(self, session):
        self.session = session

    # Create a new message
    def create(self, payload):
        msg = Message(payload=payload, status='pending')
        self.session.add(msg)
        self.session.commit()
        self.session.refresh(msg)
        return msg

    # Retrieve a message by ID
    def get(self, message_id):
        return self.session.get(Message, message_id)

    # List messages (optionally filtered by status)
    def list(self, status=None):
        query = self.session.query(Message)
        if status:
            query = query.filter(Message.status == status)
        return query.order_by(Message.created_at.desc()).all()

    # Return overall stats
    def stats(self):
        total = self.session.query(Message).count()
        pending = self.session.query(Message).filter(Message.status == 'pending').count()
        completed = self.session.query(Message).filter(Message.status == 'completed').count()
        failed = self.session.query(Message).filter(Message.status == 'failed').count()

        return {
            'total': total,
            'pending': pending,
            'completed': completed,
            'failed': failed
        }
