from xml.etree.ElementInclude import include
from routes.user import router as user_router
from fastapi import FastAPI
import uvicorn

from db.database import init_db, close_db

async def lifespan(app: FastAPI):
    await init_db()
    try:
        yield
    finally:
        await close_db()

app = FastAPI(lifespan=lifespan)

def main() -> FastAPI:

    app.include_router(user_router)


    return app

appMain = main()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)