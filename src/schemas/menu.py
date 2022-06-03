from pydantic import BaseModel


class MenuCreateSchema(BaseModel):
    title: str

    class Config:
        orm_mode = True


class MenuSchema(MenuCreateSchema):
    id: int
