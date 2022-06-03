import databases
from sqlalchemy import MetaData, create_engine
from src.settings.settings import DATABASE_URL

db = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

metadata = MetaData()
