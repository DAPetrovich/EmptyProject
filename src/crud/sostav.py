from src.models.menu import SostavModel
from src.schemas.sostav import SostavCreateSchema, SostavSchema
from src.settings.database import db


class SostavCRUD:
    async def create(data: SostavCreateSchema):
        menu_id = await db.execute(SostavModel.insert().values(**data.dict()))
        return SostavSchema(**data.dict(), id=menu_id)

    async def list(skip: int = 0, limit: int = 100):
        results = await db.fetch_all(SostavModel.select().offset(skip).limit(limit))
        return [dict(result) for result in results]

    async def delete(id: int):
        await db.execute(SostavModel.delete().where(SostavModel.c.id == id))
        return None
