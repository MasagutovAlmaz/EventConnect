import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

Base = declarative_base()

load_dotenv()

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}" \
               f"@{os.getenv('DB_HOST')}:{int(os.getenv('DB_PORT'))}/{os.getenv('DB_NAME')}"

async_engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    try:
        async with async_engine.begin() as conn:
            print("Initializing the database")
            await conn.run_sync(Base.metadata.create_all)
            print("Database initialized")
    except Exception as e:
        print(f"Error during database initialization: {e}")

async def close_db():
    await async_engine.dispose()