from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.event import Event
from models.event import EventResponse, EventCreateRequest

router = APIRouter()

@router.post("/events", response_model=EventResponse)
async def create_event(event_data: EventCreateRequest, db: AsyncSession = Depends(get_db)):
    naive_date = event_data.date.replace(tzinfo=None)

    new_event = Event(
        title=event_data.title,
        date=naive_date,
        location=event_data.location,
        timezone=event_data.timezone,
        is_active=event_data.is_active
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

    event_response_data = EventResponse.from_orm(new_event)

    return event_response_data