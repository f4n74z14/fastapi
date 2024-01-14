from typing import Annotated

from pydantic import (
    BaseModel,
    StringConstraints,
    EmailStr,
    StrictBool
)


class EasyLang(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, max_length=5, min_length=5)]

    class Config:
        from_attributes = True


class Lang(EasyLang):
    id: int
    cyrillic: StrictBool = False

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True, max_length=16, min_length=3,
                                               pattern=r'^[a-z0-9_-]{3,16}$')]
    email: Annotated[str, EmailStr]
    full_name: Annotated[str, StringConstraints(strip_whitespace=True, max_length=150, min_length=3,
                                                pattern=r'^[A-zа-яА-ЯёЁ]')]
    lang: EasyLang

    class Config:
        from_attributes = True


class User(UserCreate):
    id: int
    lang: Lang

    class Config:
        from_attributes = True
