import databases
from sqlalchemy import MetaData, create_engine

DATABASE_URL = "postgresql://postgres:postgres@localhost/postgresql"

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

metadata = MetaData()
