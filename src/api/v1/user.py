from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from src.crud.user import UserCRUD
from src.schemas.user import Token, UpdateUser, User, UserCreate
from src.settings.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):

    user = await UserCRUD.authenticate_user(form_data.username, form_data.password)
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
async def create_user(user: UserCreate):
    """Создаём пользователя. Если email был то возвращаем ошибку"""
    db_user = await UserCRUD.get_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await UserCRUD.create(user)


@router.get("/", response_model=List[User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    access=Depends(UserCRUD.get_current_active_user),
):
    return await UserCRUD.list(skip=skip, limit=limit)


@router.patch("/{id}", response_model=User)
async def patch_users(
    user: UpdateUser,
    id: int,
    access=Depends(UserCRUD.get_current_active_user),
):
    return await UserCRUD.user_patch(id, user)


@router.delete("/{id}")
async def delete_users(
    id: int,
    access=Depends(UserCRUD.get_current_active_user),
):
    await UserCRUD.delete(id)
    return Response(status_code=status.HTTP_200_OK)
