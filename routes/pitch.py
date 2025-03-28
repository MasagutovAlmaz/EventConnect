from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.pitch import Pitch
from models.pitch import ResponsePitches

router = APIRouter(tags=["pitch"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/pitches")
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
    if len(file_content) > 100 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Файл слишком большой (максимум 100 МБ)")

    new_pitch = Pitch(
        city=city,
        name_startup=name_startup,
        url_site=url_site,
        stage=stage,
        description_startup=description_startup,
        business=business,
        Presentation=presentation
    )

    if not isinstance(new_pitch.Presentation, str) or not new_pitch.Presentation.strip():
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
