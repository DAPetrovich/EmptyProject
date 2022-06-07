from sqlalchemy import delete, select
from src.models.menu import IngredietModel
from src.schemas.ingredient import IngredientCreateSchema
from src.settings.database import async_session


class IngredientCRUD:
    async def create(data: IngredientCreateSchema):
        async with async_session() as session:
            value = IngredietModel(**data.dict())
            session.add(value)
            await session.commit()
            await session.refresh(value)
        return value

    async def list(skip: int = 0, limit: int = 100):
        async with async_session() as session:
            results = await session.execute(select(IngredietModel))
        return results.scalars().all()

    async def delete(id: int):
        async with async_session() as session:
            await session.execute(delete(IngredietModel).where(IngredietModel.id == id))
            await session.commit()
        return None
