from datetime import datetime
from pydantic import BaseModel, field_validator, PrivateAttr


class EventCreateRequest(BaseModel):
    title: str
    date: datetime
    location: str
    is_active: bool = True
    timezone: str = "UTC+3"
    image_url: str

    @field_validator('date')
    def truncate_seconds(cls, v):
        return v.replace(second=0, microsecond=0)

class EventResponse(BaseModel):
    id: int
    title: str
    date: datetime
    location: str
    participants_count: int = 0
    timezone: str = "UTC+3"
    image_url: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M"),
            int: lambda v: None if v == 0 else v # убрал participants_count
        }

class GetEventResponse(BaseModel):
    id: int
    participants_count: int = 0