import sqlalchemy as sa
from src.settings.database import metadata

UserModel = sa.Table(
    "UserModel",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("username", sa.String),
    sa.Column("email", sa.String, unique=True, index=True),
    sa.Column("full_name", sa.String),
    sa.Column("disabled", sa.Boolean, default=True),
    sa.Column("password", sa.String),
    sa.Column("is_active", sa.Boolean, default=True),
)
