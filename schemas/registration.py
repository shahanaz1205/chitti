from pydantic import BaseModel
from datetime import datetime

class RegistrationCreate(BaseModel):
    event_id: int


class RegistrationOut(BaseModel):
    id: int
    event_id: int
    user_id: int
    registered_at: datetime
    status: str

    class Config:
        from_attributes = True