import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.models import Register
from models.user import RegistrationRequest, RegisterResponse

router = APIRouter()


@router.post("/register", tags=["user"])
async def register(data: RegistrationRequest, db: AsyncSession = Depends(get_db)):
    if not data.agree_personal_data or not data.agree_terms:
        raise HTTPException(status_code=400, detail="Необходимо согласие с условиями")


    new_registration = Register(
        full_name=data.full_name,
        email=str(data.email),
        phone=data.phone,
        telegram=data.telegram,
        company=data.company,
        agree_personal_data=data.agree_personal_data,
        agree_terms=data.agree_terms,
    )
    db.add(new_registration)
    try:
        await db.commit()
        await db.refresh(new_registration)
    except Exception as e:
        logging.error(f"Ошибка при сохранении пользователя: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

    reg_response = RegisterResponse.from_orm(new_registration)

    return reg_response