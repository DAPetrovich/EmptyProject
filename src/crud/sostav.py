from sqlalchemy import delete, select
from src.models.menu import SostavModel
from src.schemas.sostav import SostavCreateSchema
from src.settings.database import async_session


class SostavCRUD:
    async def create(data: SostavCreateSchema):
        async with async_session() as session:
            value = SostavModel(**data.dict())
            session.add(value)
            await session.commit()
            await session.refresh(value)
        return value

    async def list(skip: int = 0, limit: int = 100):
        async with async_session() as session:
            results = await session.execute(select(SostavModel))
        return results.scalars().all()

    async def delete(id: int):
        async with async_session() as session:
            await session.execute(delete(SostavModel).where(SostavModel.id == id))
            await session.commit()
        return None
