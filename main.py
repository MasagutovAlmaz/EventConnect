from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

from routes.registration import router as event_register_router
from routes.event import router as event_router
from routes.user import router as user_router
from routes.pitch import router as pitch_router
from fastapi import FastAPI
import uvicorn
from db.database import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    try:
        yield
    finally:
        await close_db()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def main() -> FastAPI:

    app.include_router(event_register_router)
    app.include_router(event_router)
    app.include_router(user_router)
    app.include_router(pitch_router)


    return app

appMain = main()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)