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
                results_2 = await session.execute(
                    sa.select(SostavModel, IngredietModel)
                    .join(IngredietModel)
                    .where(SostavModel.menu == val.id)
                )
                data_2 = results_2.scalars().all()
                for val_2 in data_2:
                    result_ingredient = await session.execute(
                        sa.select(IngredietModel).where(
                            IngredietModel.id == val_2.ingredients
                        )
                    )
                    data_ingredient = result_ingredient.scalars().first()

                    symmary["sostav"].append(
                        {
                            "ingredients": val_2.ingredients,
                            "amount": val_2.amount,
                            "title": data_ingredient.title,
                        },
                    )
                list_data.append(symmary)
        return list_data
