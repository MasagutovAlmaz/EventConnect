from pydantic import BaseModel, EmailStr


class RegistrationRequest(BaseModel):

    """
    Модель запроса на регистрацию пользователя
    {
  "full_name": "Иванов Иван Иванович",
  "email": "ivanov062@gmail.com",
  "phone": "+79232363096",
  "telegram": "@ivanov23",
  "company": "-", тут company по желанию, если есть
  "agree_personal_data": true, тут мы не пропускаем дальше если не стоит галочка
  "agree_terms": true, тут мы не пропускаем дальше если не стоит галочка
}
    """
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
