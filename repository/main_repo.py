from typing import Type, Sequence, Any

from sqlalchemy import ScalarResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, sessionmaker

from config import settings
from models.database import Base, DatabaseUser, DatabaseLang

all_users = []
engine = create_async_engine(settings.build_db_url(), echo=True)
AsyncSessionFactory = sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession)


async def get_session():
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init():
    async with engine.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.commit()


async def fetch_all_users(session: AsyncSession) -> Sequence[DatabaseUser]:
    stmt = select(DatabaseUser)
    result = await session.execute(stmt)

    return result.scalars().all()


async def create_user(session: AsyncSession, user: DatabaseUser):
    session.add(user)
    await session.commit()
    await session.refresh(user)


async def update_user(session: AsyncSession, old: DatabaseUser, new: DatabaseUser):
    new.id = old.id  # To update they should have the same id, ensure this

    await session.merge(new)
    await session.commit()
    await session.refresh(old)


async def fetch_user(session: AsyncSession, user_id: int) -> DatabaseUser | None:
    stmt = select(DatabaseUser).where(DatabaseUser.id == user_id)
    result = await session.execute(stmt)

    try:
        return result.scalars().first()
    except NoResultFound:
        return None


async def remove_user(session: AsyncSession, user_id: int) -> DatabaseUser | None:
    user = await fetch_user(session, user_id)

    if user is None:
        return None

    await session.delete(user)
    await session.commit()

    return user


async def fetch_lang_by_name(session: AsyncSession, lang_name: str) -> DatabaseLang | None:
    stmt = select(DatabaseLang).where(DatabaseLang.name == lang_name)
    result = await session.execute(stmt)

    try:
        return result.scalars().first()
    except NoResultFound:
        return None


async def fetch_all_langs(session: AsyncSession) -> Sequence[DatabaseLang]:
    stmt = select(DatabaseLang)
    result = await session.execute(stmt)

    return result.scalars().all()


async def fetch_lang(session: AsyncSession, lang_id: int) -> DatabaseLang | None:
    stmt = select(DatabaseLang).where(DatabaseLang.id == lang_id)
    result = await session.execute(stmt)

    try:
        return result.scalars().first()
    except NoResultFound:
        return None


async def create_lang(session: AsyncSession, lang: DatabaseLang):
    session.add(lang)
    await session.commit()
    await session.refresh(lang)


async def update_lang(session: AsyncSession, old: DatabaseLang, new: DatabaseLang):
    new.id = old.id  # To update they should have the same id, ensure this

    await session.merge(new)
    await session.commit()
    await session.refresh(old)


async def remove_lang(session: AsyncSession, lang_id: int) -> DatabaseUser | None:
    user = await fetch_lang(session, lang_id)

    if user is None:
        return None

    await session.delete(user)
    await session.commit()

    return user
