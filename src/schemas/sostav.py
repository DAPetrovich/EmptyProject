from pydantic import BaseModel


class SostavCreateSchema(BaseModel):
    ingredients: int
    menu: int
    amount: int

    class Config:
        orm_mode = True


class SostavSchema(SostavCreateSchema):
    id: int
