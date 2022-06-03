from fastapi import FastAPI

from src.api.routes import api_router
from src.database import database, engine
from src.models import menu, user

menu.metadata.create_all(bind=engine)
user.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Routers
app.include_router(api_router)
