from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from src.crud.menu import MenuCRUD
from src.crud.user import UserCRUD
from src.database import get_db
from src.schemas.menu import MenuCreateSchema, MenuSchema

router = APIRouter()


@router.get("/", response_model=List[MenuSchema])
def list_menu(
    db: Session = Depends(get_db),
):
    return MenuCRUD.list(db)


@router.post("/", response_model=MenuSchema)
def menu_create(
    data_menu: MenuCreateSchema,
    db: Session = Depends(get_db),
    # access=Depends(UserCRUD.get_current_active_user),
):
    return MenuCRUD.create(db, data_menu)


@router.delete("/{id}")
def menu_delete(
    id: int,
    db: Session = Depends(get_db),
):
    MenuCRUD.delete(db, id)
    return Response(status_code=status.HTTP_200_OK)
