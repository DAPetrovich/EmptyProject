from fastapi import APIRouter
from src.api.v1 import ingredient, menu, sostav, summary, user

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(menu.router, prefix="/menu", tags=["menu"])
api_router.include_router(ingredient.router, prefix="/ingredient", tags=["ingredient"])
api_router.include_router(sostav.router, prefix="/sostav", tags=["sostav"])
api_router.include_router(summary.router, prefix="/summary", tags=["summary"])
