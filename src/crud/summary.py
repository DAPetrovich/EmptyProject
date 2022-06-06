from src.models.menu import IngredietModel, MenuModel, SostavModel
from src.settings.database import db


class SummaryCRUD:
    async def list(skip: int = 0, limit: int = 100):

        query = MenuModel.select().offset(skip).limit(limit)
        results = await db.fetch_all(query)
        data_menu = [dict(result) for result in results]

        for val in data_menu:
            subquery = (
                SostavModel.join(IngredietModel)
                .select()
                .where(SostavModel.c.menu == val["id"])
            )
            results = await db.fetch_all(subquery)
            val["sostav"] = [dict(result) for result in results]

        return data_menu
