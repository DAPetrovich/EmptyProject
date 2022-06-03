from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import UserModel
from src.schemas.user import TokenData, UpdateUser, User, UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


class UserCRUD:
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(db, username: str, password: str):
        user = UserCRUD.get_user(db, username)
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

    def get_user(db: Session, username: str):
        return db.query(UserModel).filter(UserModel.username == username).first()

    def get_current_user(
        db: Session = Depends(get_db),
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

        user = UserCRUD.get_user(db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def get_current_active_user(
        current_user: User = Depends(get_current_user),
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    def get_by_email(db: Session, email: str):
        return db.query(UserModel).filter(UserModel.email == email).first()

    def list(db: Session, skip: int = 0, limit: int = 100):
        return db.query(UserModel).offset(skip).limit(limit).all()

    def create(db: Session, user: UserCreate):
        user.password = pwd_context.hash(user.password)
        db_user = UserModel(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def user_patch(db: Session, id: int, user: UpdateUser):
        db.query(UserModel).filter(UserModel.id == id).update(user.dict())
        db.commit()
        return db.query(UserModel).filter(UserModel.id == id).first()

    def delete(db: Session, id: int):
        db.query(UserModel).filter(UserModel.id == id).delete()
        db.commit()
        return None
