from src.models.menu import IngredietModel
from src.schemas.ingredient import IngredientCreateSchema, IngredientSchema
from src.settings.database import db


class IngredientCRUD:
    async def create(val: IngredientCreateSchema):
        menu_id = await db.execute(IngredietModel.insert().values(**val.dict()))
        return IngredientSchema(**val.dict(), id=menu_id)

    async def list(skip: int = 0, limit: int = 100):
        results = await db.fetch_all(IngredietModel.select().offset(skip).limit(limit))
        return [dict(result) for result in results]

    async def delete(id: int):
        await db.execute(IngredietModel.delete().where(IngredietModel.c.id == id))
        return None
