from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse

from routes.registration import router as event_register_router
from routes.event import router as event_router
from routes.pitch import router as pitch_router
from fastapi import FastAPI, Request
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


origins = [
    "http://localhost:3000",
    "https://af4f-78-92-147-86.ngrok-free.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],
)

def main() -> FastAPI:
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Слишком много запрос, дождитесь перезагрузки."},
        )

    app.include_router(event_register_router)
    app.include_router(event_router)
    app.include_router(pitch_router)


    return app

appMain = main()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)