from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.crud.user import ACCESS_TOKEN_EXPIRE_MINUTES, UserCRUD
from src.database import get_db
from src.schemas.user import Token, UpdateUser, User, UserCreate

router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = UserCRUD.authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserCRUD.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def read_users_me(
    current_user: User = Depends(UserCRUD.get_current_active_user),
):
    return current_user


@router.post("/", response_model=User)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """Создаём пользователя. Если email был то возвращаем ошибку"""
    db_user = UserCRUD.get_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserCRUD.create(db, user)


@router.get("/", response_model=List[User])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return UserCRUD.list(db, skip=skip, limit=limit)


@router.patch("/{id}", response_model=User)
def patch_users(
    user: UpdateUser,
    id: int,
    db: Session = Depends(get_db),
    access=Depends(UserCRUD.get_current_active_user),
):
    return UserCRUD.user_patch(db, id, user)


@router.delete("/{id}")
def delete_users(
    id: int,
    db: Session = Depends(get_db),
):
    UserCRUD.delete(db, id)
    return Response(status_code=status.HTTP_200_OK)
