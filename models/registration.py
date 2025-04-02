from typing import Optional

from pydantic import BaseModel, EmailStr


class EventRegistration(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    telegram: str
    company: Optional[str] = None
    agree_personal_data: bool
    agree_terms: bool
    event_id: int

class EventResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    telegram: str
    company: Optional[str] = None
    event_id: int

    class Config:
        from_attributes = True
