from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine,text
from sqlmodel.ext.asyncio.session import AsyncSession
from app.books.models import Book
from app.config import settings

engine = AsyncEngine(
    create_engine(
        url=settings.DATABASE_URL,
        echo=True
        )
    )

async def init_db():
    async with engine.begin() as conn:
        
        await conn.run_sync(SQLModel.metadata.create_all)