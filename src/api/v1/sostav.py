from typing import List

from fastapi import APIRouter, Response, status
from src.crud.sostav import SostavCRUD
from src.schemas.sostav import SostavCreateSchema, SostavSchema

router = APIRouter()


@router.get("/", response_model=List[SostavSchema])
async def list(skip: int = 0, limit: int = 100):
    return await SostavCRUD.list(skip=skip, limit=limit)


@router.post("/", response_model=SostavCreateSchema)
async def create(data_menu: SostavCreateSchema):
    return await SostavCRUD.create(data_menu)


@router.delete("/{id}")
async def delete(id: int):
    await SostavCRUD.delete(id)
    return Response(status_code=status.HTTP_200_OK)
