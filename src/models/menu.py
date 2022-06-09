import sqlalchemy as sa
from sqlalchemy.orm import relationship
from src.settings.database import Base


class MenuModel(Base):
    __tablename__ = "menu"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String)


class SostavModel(Base):
    __tablename__ = "sostav"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    ingredients_id = sa.Column(sa.Integer, sa.ForeignKey("ingredient.id"))
    menu_id = sa.Column(sa.Integer, sa.ForeignKey("menu.id"))
    amount = sa.Column(sa.DECIMAL(precision=5, scale=2), default=0)
    user = relationship("MenuModel", backref="sostav")
    ingredient = relationship("IngredietModel", backref="sostav")


class IngredietModel(Base):
    __tablename__ = "ingredient"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String)
