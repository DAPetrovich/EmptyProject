from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from src.api.routes import api_router
from src.models.user import UserModel

app = FastAPI()


@app.middleware("http")
async def security(request: Request, call_next):
    """
    Если токен пришёл, то идём дальше.
    иначе возвращаем ошибку не авторизован
    """
    if request.url.path in ("/docs", "/openapi.json", "/create_admin_for_test"):
        response: Response = await call_next(request)
        return response

    if request.headers.get("authorization"):
        # тут нужно было бы проверить сам токен на валидность
        response: Response = await call_next(request)
        return response
    else:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})


@app.post(
    "/create_admin_for_test",
    tags=["Start"],
    description="создаём пользователя для авторизации: username: admin, password: pass",
)
async def create_user():
    from sqlalchemy import insert

    from src.settings.database import async_session

    user_dict = {
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Adminovich",
        "disabled": False,
        "is_active": True,
        "password": "$2b$12$FfszLKST1RX5cMEHoC13LexcWU8vrY.wel8GyiCkiBnGEtgv1H3zW",
    }

    async with async_session() as session:
        await session.execute(insert(UserModel).values(**user_dict))
        await session.commit()
    return None


# Routers
app.include_router(api_router)
