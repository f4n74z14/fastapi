from typing import Annotated

from pydantic import BaseModel, StringConstraints, EmailStr


class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True, pattern=r'^[\w]{3,16}$')]
    email: Annotated[str, EmailStr]
    full_name: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r'^[A-z]([-\']?[A-z]+)*( [A-z]([-\']?[A-z]+)*)+$')]


class User(UserCreate):
    id: int

    def update(self, updated_data: UserCreate):
        self.username = updated_data.username
        self.email = updated_data.email
        self.full_name = updated_data.full_name

