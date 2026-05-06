from sqlalchemy import Column, Integer, String, Text
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    venue = Column(String, nullable=False)
    event_date = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)