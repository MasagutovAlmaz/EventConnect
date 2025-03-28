from pydantic import BaseModel, Field

class ResponsePitches(BaseModel):
    id: int
    city: str
    name_startup: str
    url_site: str
    stage: str
    description_startup: str
    business: str
    presentation: str

class RequestContactData(BaseModel):
    name: str
    second_name: str
    email: str
    phone: str
    url_social_media: str
    agree_terms: bool

class ResponseContactData(BaseModel):
    id: int
    name: str
    second_name: str
    email: str
    phone: str
    url_social_media: str
    agree_terms: bool