from typing import List, Optional

from pydantic import BaseModel, condecimal


class SostavSchema(BaseModel):
    ingredients: int
    title: str
    amount: Optional[condecimal(max_digits=5, decimal_places=2)]


class SummarySchema(BaseModel):
    id: int
    title: str
    sostav: List[SostavSchema]

    class Config:
        orm_mode = True
