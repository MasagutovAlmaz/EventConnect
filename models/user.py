from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_verified: bool

    class Config:
        from_attributes = True

class RegisterResponse(BaseModel):
    message: str
    user: UserResponse

class Token(BaseModel):
    access_token: str
    token_type: str

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str