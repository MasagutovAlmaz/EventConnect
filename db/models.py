from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, validates, relationship

Base = declarative_base()

class RegisterEvent(Base):
    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    telegram = Column(String, index=True)
    company = Column(String, index=True, nullable=True)
    agree_personal_data = Column(Boolean, index=True)
    agree_terms = Column(Boolean, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="registrations")

    @validates('agree_personal_data', 'agree_terms')
    def validate_agreements(self, _, value):
        if not value:
            raise ValueError("Необходимо согласиться с условиями")
        return value


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






