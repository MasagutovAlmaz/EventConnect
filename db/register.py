from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import validates, relationship

from db import Base


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