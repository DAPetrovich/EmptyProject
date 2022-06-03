import sqlalchemy as sa
from sqlalchemy import Boolean, Integer, String
from src.database import Base


class UserModel(Base):
    __tablename__ = "user"

    id = sa.Column(Integer, primary_key=True, index=True)
    username = sa.Column(String)
    email = sa.Column(String, unique=True, index=True)
    full_name = sa.Column(String)
    disabled = sa.Column(Boolean, default=True)
    password = sa.Column(String)
    is_active = sa.Column(Boolean, default=True)
