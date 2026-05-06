from pydantic import BaseModel

class EventCreate(BaseModel):
    title: str
    description: str
    venue: str
    event_date: str
    max_participants: int


class EventOut(BaseModel):
    id: int
    title: str
    description: str
    venue: str
    event_date: str
    max_participants: int

    class Config:
        from_attributes = True