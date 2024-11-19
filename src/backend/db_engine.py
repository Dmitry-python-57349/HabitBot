from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.settings import settings

async_engine = create_async_engine(
    url=settings.get_db_url,
    echo=True,
)

async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    ...
