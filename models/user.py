from pydantic import BaseModel, EmailStr


class RegistrationRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    telegram: str
    company: str | None = None
    agree_personal_data: bool
    agree_terms: bool

class RegisterResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    telegram: str
    company: str | None = None

    class Config:
        from_attributes = True
