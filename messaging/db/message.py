from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Text, DateTime
from messaging.db.base import Base


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, index=True)
    payload = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default='pending')
    result = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(UTC),
                        onupdate=lambda: datetime.now(UTC))  # ensures your timestamps are accurate

    def __repr__(self):
        return f'<Message id={self.id} status={self.status}>'
