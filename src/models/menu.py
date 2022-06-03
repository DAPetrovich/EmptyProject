import sqlalchemy as sa
from src.database import Base


class MenuModel(Base):
    __tablename__ = "menu"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String)
    sostav = sa.Column(sa.Integer, sa.ForeignKey("sostav.id"))


class SostavModel(Base):
    __tablename__ = "sostav"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    ingredients = sa.Column(sa.Integer, sa.ForeignKey("ingredient.id"))


class IngredietModel(Base):
    __tablename__ = "ingredient"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String)
