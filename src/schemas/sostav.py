from typing import Optional

from pydantic import BaseModel, condecimal


class SostavCreateSchema(BaseModel):
    ingredients: int
    menu: int
    amount: Optional[condecimal(max_digits=5, decimal_places=2)]

    class Config:
        orm_mode = True


class SostavSchema(SostavCreateSchema):
    id: int
