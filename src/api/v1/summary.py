from typing import List

from fastapi import APIRouter
from src.crud.summary import SummaryCRUD
from src.schemas.summary import SummarySchema

router = APIRouter()


@router.get("/", response_model=List[SummarySchema])
async def list(skip: int = 0, limit: int = 100):
    return await SummaryCRUD.list(skip=skip, limit=limit)
