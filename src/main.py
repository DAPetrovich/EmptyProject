from fastapi import FastAPI

from src.api.routes import api_router
from src.database import engine
from src.models import menu, user

menu.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(api_router)
