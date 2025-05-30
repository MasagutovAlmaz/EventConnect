from time import timezone

from sqlalchemy import Column, String, Boolean, Integer, DateTime, select, func, Sequence
from sqlalchemy.orm import relationship, column_property

from db.registration import Base, RegisterEvent



class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    current_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String, nullable=False)
    timezone = Column(String, default="UTC+3")
    is_active = Column(Boolean, default=True)
    image_url = Column(String, nullable=False)
    time = Column(String, nullable=True)

    registrations = relationship("RegisterEvent", back_populates="event")

    def __init__(self, **kwargs):
        if 'date' in kwargs and kwargs['date']:
            kwargs['date'] = kwargs['date'].replace(second=0, microsecond=0)
        super().__init__(**kwargs)

    participants_count = column_property(
        select(func.count())
        .where(RegisterEvent.event_id == id)
        .scalar_subquery()
    )