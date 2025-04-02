from datetime import datetime

from pydantic import BaseModel, root_validator


class EventCreateRequest(BaseModel):
    title: str
    date: datetime
    current_date: datetime
    end_date: datetime
    location: str
    is_active: bool = True
    timezone: str = "UTC+3"
    image_url: str
    time: str = "19:00"

class EventResponse(BaseModel):
    id: int
    title: str
    date: datetime
    current_date: datetime
    end_date: datetime
    is_active: bool
    location: str
    participants_count: int = 0
    timezone: str = "UTC+3"
    image_url: str
    time: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M"),
            int: lambda v: None if v == 0 else v # убрал participants_count
        }

class GetEventParticipantCountResponse(BaseModel):
    id: int
    participants_count: int = 0

class GetEventResponse(BaseModel):
    id: int
    title: str
    date: datetime
    current_date: datetime
    end_date: datetime
    location: str
    image_url: str
    is_active: bool
    time: str
    timezone: str = "UTC+3"
