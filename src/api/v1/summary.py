from typing import List

from fastapi import APIRouter, Depends
from src.crud.summary import SummaryCRUD
from src.crud.user import UserCRUD
from src.schemas.summary import SummarySchema

router = APIRouter()


@router.get("/", response_model=List[SummarySchema])
async def list(
    skip: int = 0,
    limit: int = 100,
    access=Depends(UserCRUD.get_current_active_user),
):
    return await SummaryCRUD.list(skip=skip, limit=limit)


@router.get("/temp", response_model=List[SummarySchema])
async def list_temp(
    skip: int = 0,
    limit: int = 100,
    access=Depends(UserCRUD.get_current_active_user),
):
    return await SummaryCRUD.list_temp(skip=skip, limit=limit)
