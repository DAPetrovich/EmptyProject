from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: Union[str, None] = None
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    is_active: Union[bool, None] = None

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    is_active: Union[bool, None] = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    is_active: Union[bool, None] = None
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
