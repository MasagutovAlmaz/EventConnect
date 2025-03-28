from pathlib import Path

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from db.event import Event
from models.event import EventResponse, EventCreateRequest, GetEventResponse

router = APIRouter(tags=["event"])

@router.post("/events", response_model=EventResponse)
async def create_event(event_data: EventCreateRequest, db: AsyncSession = Depends(get_db)):
    naive_date = event_data.date.replace(tzinfo=None)

    new_event = Event(
        title=event_data.title,
        date=naive_date,
        location=event_data.location,
        timezone=event_data.timezone,
        is_active=event_data.is_active,
        image_url=event_data.image_url
    )

    db.add(new_event)
    try:
        await db.commit()
        await db.refresh(new_event)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании мероприятия: {str(e)}"
        )


    event_response_data = EventResponse(**new_event.__dict__)

    return event_response_data

@router.get("/events/{event_id}", response_model=GetEventResponse)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мероприятие не найдено")
    event_response = EventResponse(**event.__dict__)

    return event_response