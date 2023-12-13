from typing import List

from fastapi import APIRouter
from fastapi.params import Path

from repository import users_database
from exceptions import exceptions
from models.user import User, UserCreate
from responses import responses

router = APIRouter()


@router.get("/api/users/", response_model=List[User])
async def get_users():
    return users_database.all_users


@router.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = users_database.find_user(user_id)

    if user is None:
        raise exceptions.USER_NOT_FOUND

    return user


@router.post("/api/users/", response_model=User)
async def create_user(user: UserCreate):
    actual_user = User(**user.model_dump(), id=len(users_database.all_users) + 1)
    users_database.all_users.append(actual_user)

    return actual_user


@router.put("/api/users/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: UserCreate):
    user = users_database.find_user(user_id)

    if user is None:
        raise exceptions.USER_NOT_FOUND

    user.update(updated_user)
    return user


@router.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    removed_user = users_database.remove_user(user_id)

    if removed_user is None:
        raise exceptions.USER_NOT_FOUND

    return responses.USER_DELETED_SUCCESSFULLY
