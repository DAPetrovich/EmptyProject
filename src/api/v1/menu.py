from typing import List

from fastapi import APIRouter, Response, status
from src.crud.menu import MenuCRUD
from src.schemas.menu import MenuCreateSchema, MenuSchema

router = APIRouter()


@router.get("/", response_model=List[MenuSchema])
async def list_menu(skip: int = 0, limit: int = 100):
    return await MenuCRUD.list(skip=skip, limit=limit)


@router.post("/", response_model=MenuSchema)
async def menu_create(data_menu: MenuCreateSchema):
    return await MenuCRUD.create(data_menu)


@router.delete("/{id}")
async def menu_delete(id: int):
    await MenuCRUD.delete(id)
    return Response(status_code=status.HTTP_200_OK)
