from sqlalchemy import Column, String, Enum, Integer

from db.database import Base


class Pitch(Base):
    __tablename__ = "pitches"

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=True)
    name_startup = Column(String, nullable=True)
    url_site = Column(String, nullable=True)
    stage = Column(Enum("Идея", "MVP", "Компания с первыми продажами", "Растущую компания", name="name_startup"), nullable=True)
    description_startup = Column(String(300), nullable=True)
    business = Column(String(500), nullable=True)
    Presentation = Column(String, nullable=True)

