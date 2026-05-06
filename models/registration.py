from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from database import Base
from datetime import datetime

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    registered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Confirmed")