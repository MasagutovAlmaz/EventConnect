from xmlrpc.client import boolean

from sqlalchemy import Column, String, Enum, Integer, Boolean

from db.database import Base


class RequestPitch(Base):
    __tablename__ = "request_pitch"

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=True)
    name_startup = Column(String, nullable=True)
    url_site = Column(String, nullable=True)
    stage = Column(Enum("Идея", "MVP", "Компания с первыми продажами", "Растущую компания", name="name_startup"), nullable=True)
    description_startup = Column(String(300), nullable=True)
    business = Column(String(500), nullable=True)
    presentation = Column(String, nullable=True)

class ContactDataForPitch(Base):
    __tablename__ = "contact_data_for_pitch"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    url_social_media = Column(String, nullable=True)
    agree_terms = Column(Boolean, index=True)
