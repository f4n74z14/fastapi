from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import DatabaseUser, DatabaseLang
from repository import main_repo
from exceptions import exceptions
from models.schema import User, UserCreate
from responses import responses

router = APIRouter(prefix="/api/users")


@router.get("/", response_model=list[User])
async def get_users(session: AsyncSession = Depends(main_repo.get_session)):
    return await main_repo.fetch_all_users(session)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, session: AsyncSession = Depends(main_repo.get_session)):
    user = await main_repo.fetch_user(session, user_id)

    if user is None:
        raise exceptions.USER_NOT_FOUND

    return user


@router.post("/", response_model=User)
async def create_user(user: UserCreate, session: AsyncSession = Depends(main_repo.get_session)):
    fetched_lang = await main_repo.fetch_lang_by_name(session, user.lang.name)

    if fetched_lang is None:
        raise HTTPException(status_code=404, detail=f"Язык '{user.lang.name}' не найден.")

    database_user = DatabaseUser(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        lang_id=fetched_lang.id
    )

    await main_repo.create_user(session, database_user)

    return database_user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: UserCreate, session: AsyncSession = Depends(main_repo.get_session)):
    database_user = await main_repo.fetch_user(session, user_id)
    fetched_lang = await main_repo.fetch_lang_by_name(session, updated_user.lang.name)

    if fetched_lang is None:
        raise HTTPException(status_code=404, detail=f"Язык '{updated_user.lang.name}' не найден.")

    if database_user is None:
        raise exceptions.USER_NOT_FOUND

    await main_repo.update_user(session, database_user, DatabaseUser(
        username=updated_user.username,
        email=updated_user.email,
        full_name=updated_user.full_name,
        lang_id=fetched_lang.id
    ))

    return database_user


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(main_repo.get_session)):
    removed_user = await main_repo.remove_user(session, user_id)

    if removed_user is None:
        raise exceptions.USER_NOT_FOUND

    return responses.USER_DELETED_SUCCESSFULLY
