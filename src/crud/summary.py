import sqlalchemy as sa
from src.models.menu import IngredietModel, MenuModel, SostavModel
from src.settings.database import async_session


class SummaryCRUD:
    """TODO подумать как уменьшить количество запросов"""

    async def list(skip: int = 0, limit: int = 100):
        async with async_session() as session:
            results = await session.execute(sa.select(MenuModel))
            data = results.scalars().all()
            list_data = []
            for val in data:
                symmary = {
                    "id": val.id,
                    "title": val.title,
                    "sostav": [],
                }
                subquery = await session.execute(
                    sa.select(SostavModel, IngredietModel)
                    .join(IngredietModel)
                    .where(SostavModel.menu == val.id)
                )
                subquery_data = subquery.all()
                for row in subquery_data:
                    symmary["sostav"].append(
                        {
                            "ingredients": row.SostavModel.ingredients,
                            "amount": row.SostavModel.amount,
                            "title": row.IngredietModel.title,
                        },
                    )
                list_data.append(symmary)
            await session.commit()
        return list_data

    async def list_temp(skip: int = 0, limit: int = 100):
        """Подопытная ручка)))"""
        async with async_session() as session:
            query = (
                sa.select(SostavModel, MenuModel, IngredietModel)
                .join(MenuModel)
                .join(IngredietModel)
                .order_by(MenuModel.id)
            )
            results = await session.execute(query)
            data = results.all()
            list_row = [dict(result) for result in data]
            for row in list_row:
                print(
                    row["SostavModel"].id,
                    row["SostavModel"].ingredients,
                    row["SostavModel"].menu,
                    row["SostavModel"].amount,
                    row["MenuModel"].title,
                    row["MenuModel"].id,
                    row["IngredietModel"].title,
                    row["IngredietModel"].id,
                )

            await session.commit()
        return None
