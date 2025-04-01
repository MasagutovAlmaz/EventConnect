from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from db.event import Event
from models.event import EventResponse, EventCreateRequest, GetEventParticipantCountResponse, GetEventResponse

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
        image_url=event_data.image_url,
        time=event_data.time
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

@router.get("/events/count/{event_id}", response_model=GetEventParticipantCountResponse)
async def get_even_participant_count(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мероприятие не найдено")
    event_response = EventResponse(**event.__dict__)

    return event_response

@router.get("/events/all", response_model=list[GetEventResponse])
async def get_event_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event))
    events = result.scalars().all()

    return [GetEventResponse(**event.__dict__) for event in events]

@router.get("/events/{event_id}", response_model=GetEventResponse)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мероприятие не найдено")

    event_response = EventResponse(**event.__dict__)

    return event_response

@router.delete("/events/{event_id}")
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мероприятие не найдено")

    await db.delete(event)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении мероприятия: {str(e)}"
        )

    return {"detail": "Мероприятие успешно удалено"}

@router.put("/events/{event_id}", response_model=EventResponse)
async def update_event(event_id: int, event_data: EventCreateRequest, db: AsyncSession = Depends(get_db)):
    event = await db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мероприятие не найдено")

    naive_date = event_data.date.replace(tzinfo=None)

    event.title = event_data.title
    event.date = naive_date
    event.location = event_data.location
    event.timezone = event_data.timezone
    event.is_active = event_data.is_active
    event.image_url = event_data.image_url
    event.time = event_data.time

    db.add(event)
    try:
        await db.commit()
        await db.refresh(event)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении мероприятия: {str(e)}"
        )

    return EventResponse(**event.__dict__)

