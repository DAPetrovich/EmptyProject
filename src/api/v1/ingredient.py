from typing import List

from fastapi import APIRouter, Depends, Response, status
from src.crud.ingredient import IngredientCRUD
from src.crud.user import UserCRUD
from src.schemas.ingredient import IngredientCreateSchema, IngredientSchema

router = APIRouter()


@router.get("/", response_model=List[IngredientSchema])
async def list(
    skip: int = 0,
    limit: int = 100,
    access=Depends(UserCRUD.get_current_active_user),
):
    return await IngredientCRUD.list(skip=skip, limit=limit)


@router.post("/", response_model=IngredientSchema)
async def create(
    data: IngredientCreateSchema,
    access=Depends(UserCRUD.get_current_active_user),
):
    return await IngredientCRUD.create(data)


@router.delete("/{id}")
async def delete(
    id: int,
    access=Depends(UserCRUD.get_current_active_user),
):
    await IngredientCRUD.delete(id)
    return Response(status_code=status.HTTP_200_OK)
