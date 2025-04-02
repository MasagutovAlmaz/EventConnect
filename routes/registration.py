import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from db.database import get_db
from db.registration import RegisterEvent
from models.registration import EventRegistration, EventResponse

router = APIRouter(tags=["register-events"])

limiter = Limiter(key_func=get_remote_address)


@router.post("/register-event", summary="Регистрация нового пользователя",
    description="""
    ## Описание:
    Регистрирует пользователя в системе.  
    **Обязательные условия:**  
    - Пользователь должен согласиться с обработкой данных (`agree_personal_data=True`).  
    - Пользователь должен принять условия оферты (`agree_terms=True`).  

    ## Пример запроса:
    ```json
    {
      "full_name": "Иванов Иван Иванович",
      "email": "ivonov32434@gmail.com",
      "phone": "+79991234567",
      "telegram": "@ivanov233",
      "agree_personal_data": true,
      "agree_terms": true
    }
    ```
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Успешная регистрация",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "full_name": "Иванов Иван Иванович",
                        "email": "ivonov32434@gmail.com",
                        "phone": "+79991234567",
                        "telegram": "@ivanov233"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Ошибка валидации",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Необходимо согласиться с условиями"
                    }
                }
            }
        }
    }
)
@limiter.limit("5/minute")
async def register(request: Request, data: EventRegistration, db: AsyncSession = Depends(get_db)):
    if not data.agree_personal_data or not data.agree_terms:
        raise HTTPException(status_code=400, detail="Необходимо согласие с условиями")

    new_registration = RegisterEvent(**data.model_dump())
    db.add(new_registration)
    try:
        await db.commit()
        await db.refresh(new_registration)
    except Exception as e:
        logging.error(f"Ошибка при сохранении пользователя: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

    reg_response = EventResponse(**new_registration.__dict__)

    return reg_response