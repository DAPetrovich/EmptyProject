import sqlalchemy as sa
from src.settings.database import Base


class UserModel(Base):
    __tablename__ = "UserModel"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True, index=True)
    full_name = sa.Column(sa.String)
    disabled = sa.Column(sa.Boolean, default=True)
    password = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean, default=True)
