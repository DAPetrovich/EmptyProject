import sqlalchemy as sa
from src.database import metadata

MenuModel = sa.Table(
    "menu",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("title", sa.String),
    sa.Column("sostav", sa.Integer, sa.ForeignKey("sostav.id")),
)


SostavModel = sa.Table(
    "sostav",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("ingredients", sa.Integer, sa.ForeignKey("ingredient.id")),
)


IngredietModel = sa.Table(
    "ingredient",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("title", sa.String),
)
