import sqlalchemy as sa
from src.settings.database import metadata

MenuModel = sa.Table(
    "menu",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("title", sa.String),
)


SostavModel = sa.Table(
    "sostav",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("ingredients", sa.Integer, sa.ForeignKey("ingredient.id")),
    sa.Column("menu", sa.Integer, sa.ForeignKey("menu.id")),
    sa.Column("amount", sa.DECIMAL(precision=5, scale=2), default=0),
)


IngredietModel = sa.Table(
    "ingredient",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("title", sa.String),
)
