from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    telegram: str
    company: str | None = None
    event_id: int