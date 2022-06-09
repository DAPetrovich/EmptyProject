from fastapi import FastAPI

from src.api.routes import api_router

app = FastAPI()


# Routers
app.include_router(api_router)
