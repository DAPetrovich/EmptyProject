from fastapi import FastAPI

from src.api.routes import api_router
from src.settings.database import db, engine, metadata

metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


# Routers
app.include_router(api_router)
