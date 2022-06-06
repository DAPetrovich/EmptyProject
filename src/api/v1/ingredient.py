from typing import List

from fastapi import APIRouter, Response, status
from src.crud.ingredient import IngredientCRUD
from src.schemas.ingredient import IngredientCreateSchema, IngredientSchema

router = APIRouter()


@router.get("/", response_model=List[IngredientSchema])
async def list(skip: int = 0, limit: int = 100):
    return await IngredientCRUD.list(skip=skip, limit=limit)


@router.post("/", response_model=IngredientSchema)
async def create(data: IngredientCreateSchema):
    return await IngredientCRUD.create(data)


@router.delete("/{id}")
async def delete(id: int):
    await IngredientCRUD.delete(id)
    return Response(status_code=status.HTTP_200_OK)
