from src.models.menu import MenuModel
from src.schemas.menu import MenuCreateSchema, MenuSchema
from src.settings.database import db


class MenuCRUD:
    async def create(menu: MenuCreateSchema):
        menu_id = await db.execute(MenuModel.insert().values(**menu.dict()))
        return MenuSchema(**menu.dict(), id=menu_id)

    async def list(skip: int = 0, limit: int = 100):
        results = await db.fetch_all(MenuModel.select().offset(skip).limit(limit))
        return [dict(result) for result in results]

    async def delete(id: int):
        await db.execute(MenuModel.delete().where(MenuModel.c.id == id))
        return None
