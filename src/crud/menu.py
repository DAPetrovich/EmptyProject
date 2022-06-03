from sqlalchemy.orm import Session
from src.models.menu import MenuModel
from src.schemas.menu import MenuCreateSchema


class MenuCRUD:
    def create(db: Session, menu: MenuCreateSchema):
        db_menu = MenuModel(**menu.dict())
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu

    def list(db: Session):
        return db.query(MenuModel).all()

    def delete(db: Session, id: int):
        db.query(MenuModel).filter(MenuModel.id == id).delete()
        db.commit()
        return None
