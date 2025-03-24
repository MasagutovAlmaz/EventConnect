import logging
import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.models import User
from models.user import RegisterResponse, UserCreate, UserResponse, OTPVerify, Token
from utils.security import generate_otp, get_password_hash, verify_password, create_access_token

router = APIRouter()


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_verification_email(email: str, otp: str):
    try:
        msg = MIMEText(f"Ваш код подтверждения: {otp}")
        msg["Subject"] = "Подтверждение почты"
        msg["From"] = EMAIL_HOST
        msg["To"] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_HOST, EMAIL_PASSWORD)
            server.sendmail(EMAIL_HOST, email, msg.as_string())
            logging.info("Email отправлен успешно")
    except Exception as e:
        logging.error(f"Ошибка при отправке email: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при отправке email: {e}")

@router.post("/register", response_model=RegisterResponse, tags=["register"])
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter(User.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    otp = generate_otp()
    otp_expiration = datetime.utcnow() + timedelta(minutes=15)

    hashed_password = get_password_hash(user.password)

    try:
        send_verification_email(user.email, otp)
    except Exception as e:
        logging.error(f"Ошибка при отправке письма: {e}")
        raise HTTPException(status_code=500, detail="Не удалось отправить письмо")

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        verification_code=otp,
        code_expiration=otp_expiration,
        is_verified=False
    )

    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception as e:
        logging.error(f"Ошибка при сохранении пользователя: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка сервера")

    user_response = UserResponse.model_validate(new_user)

    return {"message": "OTP отправлен на email. Введите код для верификации.", "user": user_response}



@router.post("/verify", tags=["verify"])
async def verify_otp(data: OTPVerify, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")

    if user.verification_code != data.otp:
        raise HTTPException(status_code=400, detail="Неверный OTP")

    if user.code_expiration < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Срок действия OTP истек")

    user.is_activate = True
    user.verification_code = "Verified"
    user.code_expiration = datetime.utcnow()
    db.add(user)
    await db.commit()

    return {"message": "Верификация прошла успешно"}



@router.post("/login", response_model=Token, tags=["login"])
async def login_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user_create.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(user_create.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
