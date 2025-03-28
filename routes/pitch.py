from dataclasses import Field
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.pitch import RequestPitch, ContactDataForPitch
from models.pitch import ResponsePitches, RequestContactData, ResponseContactData

router = APIRouter(tags=["pitch"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_SIZE = 100 * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf", "docx", "pptx", "txt"}

@router.post("/pitches-requests")
async def create_pitch(db: AsyncSession = Depends(get_db),
    city: str = Form(...),
    name_startup: str = Form(...),
    url_site: str = Form(...),
    stage: str = Form(...),
    description_startup: str = Form(...),
    business: str = Form(...),
    presentation: str = Form(...),
    file: UploadFile = File(...)):


    file_content = await file.read()
    if presentation:
        if file.size > MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail="Размер файла превышает 100 MB"
            )
        if file.filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Недопустимый формат файла. Допустимые форматы: .pdf, .docx, .pptx, .txt"
            )

    new_pitch = RequestPitch(
        city=city,
        name_startup=name_startup,
        url_site=url_site,
        stage=stage,
        description_startup=description_startup,
        business=business,
        presentation=presentation
    )

    if not isinstance(new_pitch.presentation, str) or not new_pitch.presentation.strip():
        raise ValueError("Строка 'Presentation' должна быть не пустой")

    db.add(new_pitch)
    try:
        await db.commit()
        await db.refresh(new_pitch)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании питча: {str(e)}"
        )

    file_path = UPLOAD_DIR / f"{new_pitch.id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file_content)

    new_pitch.presentation_file = str(file_path)
    await db.commit()

    return ResponsePitches(**vars(new_pitch))


@router.post("/pitch-contact-form", response_model=ResponseContactData)
async def create_pitch_contact_form(data: RequestContactData,db: AsyncSession = Depends(get_db)):
    if not data.agree_terms:
        raise HTTPException(status_code=400, detail="Необходимо согласие с условиями")

    new_pitch = ContactDataForPitch(
        name=data.name,
        second_name=data.second_name,
        email=data.email,
        phone=data.phone,
        url_social_media=data.url_social_media,
        agree_terms=data.agree_terms
    )

    db.add(new_pitch)
    try:
        await db.commit()
        await db.refresh(new_pitch)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании питча: {str(e)}"
        )

    pitch_response = ResponseContactData(**vars(new_pitch))

    return pitch_response