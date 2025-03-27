from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship
from db import Base


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    date = Column(DateTime(timezone=False))
    location = Column(String, nullable=False)
    timezone = Column(String, default="UTC+3")
    is_active = Column(Boolean, default=True)

    registrations = relationship("RegisterEvent", back_populates="event")

    def __init__(self, **kwargs):
        if 'date' in kwargs and kwargs['date']:
            kwargs['date'] = kwargs['date'].replace(second=0, microsecond=0)
        super().__init__(**kwargs)
