from sqlalchemy import delete, select
from src.models.menu import MenuModel
from src.schemas.menu import MenuCreateSchema
from src.settings.database import async_session


class MenuCRUD:
    async def create(data: MenuCreateSchema):
        async with async_session() as session:
            value = MenuModel(**data.dict())
            session.add(value)
            await session.commit()
            await session.refresh(value)
        return value

    async def list(skip: int = 0, limit: int = 100):
        async with async_session() as session:
            results = await session.execute(select(MenuModel))
        return results.scalars().all()

    async def delete(id: int):
        async with async_session() as session:
            await session.execute(delete(MenuModel).where(MenuModel.id == id))
            await session.commit()
        return None
