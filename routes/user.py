from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from db.registration import RegisterEvent
from models.user import UserResponse

router = APIRouter(tags=["user"])

@router.get("/user", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(RegisterEvent, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_response = UserResponse(**user.__dict__)
    return user_response
