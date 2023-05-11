from typing import Union

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

def create_engine(database_url: Union[URL, str]) -> create_async_engine:
    return create_async_engine(database_url, echo=True)

def get_session_maker(async_engine):
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession, 
                                   expire_on_commit=False, autoflush=False)

    return async_session

async def create_database(engine, metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)