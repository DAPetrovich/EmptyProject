from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from src.models.user import UserModel
from src.schemas.user import TokenData, UpdateUser, User, UserCreate
from src.settings.database import db
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

    def create_access_token(
        data: dict,
        expires_delta: Union[timedelta, None] = None,
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_user(username: str):
        return await db.fetch_one(
            UserModel.select().where(UserModel.c.username == username)
        )

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
        return await db.fetch_one(UserModel.select().where(UserModel.c.email == email))

    async def list(skip: int = 0, limit: int = 100):
        results = await db.fetch_all(UserModel.select().offset(skip).limit(limit))
        return [dict(result) for result in results]

    async def create(user: UserCreate):
        user.password = pwd_context.hash(user.password)
        user_id = await db.execute(UserModel.insert().values(**user.dict()))
        return User(**user.dict(), id=user_id)

    async def user_patch(id: int, user: UpdateUser):
        await db.execute(
            UserModel.update().where(UserModel.c.id == id).values(**user.dict())
        )

        return await db.fetch_one(UserModel.select().where(UserModel.c.id == id))

    async def delete(id: int):
        await db.execute(UserModel.delete().where(UserModel.c.id == id))
        return None
