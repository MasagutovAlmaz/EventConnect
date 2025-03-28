from pydantic import BaseModel

class ResponsePitches(BaseModel):
    id: int
    city: str
    name_startup: str
    url_site: str
    stage: str
    description_startup: str
    business: str
    Presentation: str