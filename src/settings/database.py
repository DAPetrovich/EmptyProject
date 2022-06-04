import databases
import sqlalchemy as sa
from src.settings.settings import DATABASE_URL

db = databases.Database(DATABASE_URL)

engine = sa.create_engine(DATABASE_URL)

metadata = sa.MetaData()
