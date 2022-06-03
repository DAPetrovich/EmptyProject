from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from src.crud.menu import MenuCRUD
from src.crud.user import UserCRUD
from src.schemas.menu import MenuCreateSchema, MenuSchema

router = APIRouter()


@router.get("/", response_model=List[MenuSchema])
def list_menu():
    return MenuCRUD.list()


@router.post("/", response_model=MenuSchema)
def menu_create(
    data_menu: MenuCreateSchema,
    # access=Depends(UserCRUD.get_current_active_user),
):
    return MenuCRUD.create(data_menu)


@router.delete("/{id}")
def menu_delete(
    id: int,
):
    MenuCRUD.delete(id)
    return Response(status_code=status.HTTP_200_OK)
