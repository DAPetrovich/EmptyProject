from typing import List

from fastapi import APIRouter, Depends, Response, status
from src.crud.menu import MenuCRUD
from src.crud.user import UserCRUD
from src.schemas.menu import MenuCreateSchema, MenuSchema

router = APIRouter()


@router.get("/", response_model=List[MenuSchema])
async def list_menu(
    skip: int = 0,
    limit: int = 100,
    access=Depends(UserCRUD.get_current_active_user),
):
    return await MenuCRUD.list(skip=skip, limit=limit)


@router.post("/", response_model=MenuSchema)
async def menu_create(
    data_menu: MenuCreateSchema,
    access=Depends(UserCRUD.get_current_active_user),
):
    return await MenuCRUD.create(data_menu)


@router.delete("/{id}")
async def menu_delete(
    id: int,
    access=Depends(UserCRUD.get_current_active_user),
):
    await MenuCRUD.delete(id)
    return Response(status_code=status.HTTP_200_OK)
