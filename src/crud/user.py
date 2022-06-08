from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import delete, select, update
from src.models.user import UserModel
from src.schemas.user import TokenData, UpdateUser, User, UserCreate
from src.settings.database import async_session
from src.settings.settings import ALGORITHM, SECRET_KEY, oauth2_scheme, pwd_context


class UserCRUD:
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(username: str, password: str):
        user = await UserCRUD.get_user(username)
        if not user:
            return False

        if not UserCRUD.verify_password(password, user.password):
            return False
        return user

    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_user(username: str):
        async with async_session() as session:
            results = await session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            await session.commit()
        return results.scalars().first()

    async def get_current_user(
        token: str = Depends(oauth2_scheme),
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception

        user = await UserCRUD.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def get_current_active_user(
        current_user: User = Depends(get_current_user),
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    async def get_by_email(email: str):
        async with async_session() as session:
            results = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
        return results.scalars().first()

    async def list(skip: int = 0, limit: int = 100):
        async with async_session() as session:
            results = await session.execute(select(UserModel).offset(skip).limit(limit))
        return results.scalars().all()

    async def create(user: UserCreate):
        async with async_session() as session:
            user.password = pwd_context.hash(user.password)
            value = UserModel(**user.dict())
            session.add(value)
            await session.commit()
            await session.refresh(value)
        return value

    async def user_patch(id: int, user: UpdateUser):
        async with async_session() as session:
            await session.execute(
                update(UserModel).where(UserModel.id == id).values(**user.dict())
            )
            await session.commit()
            results = await session.execute(select(UserModel).where(UserModel.id == id))

        return results.scalars().first()

    async def delete(id: int):
        async with async_session() as session:
            await session.execute(delete(UserModel).where(UserModel.id == id))
            await session.commit()
        return None
