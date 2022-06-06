from pydantic import BaseModel


class IngredientCreateSchema(BaseModel):
    title: str

    class Config:
        orm_mode = True


class IngredientSchema(IngredientCreateSchema):
    id: int
