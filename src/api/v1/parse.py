import asyncio
import os
from time import time

import aiohttp
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from requests import Session
from src.crud.user import UserCRUD

router = APIRouter()

load_dotenv("src\.env")
env = os.environ


account_id = env.get("ACCOUNT_ID")
access_token = env.get("HUNTFLOW_TOKEN")
company_mail = env.get("COMPANY_EMAIL")
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {}".format(access_token),
    "User-Agent": "App/1.0 ({})".format(company_mail),
}


async def async_get_list(url_huntflow, vacansy_id):
    async with aiohttp.ClientSession() as session:
        session.headers.update(headers)
        async with session.get(url_huntflow, params={"vacancy": vacansy_id}) as response:
            data = await response.text()


async def async_get():
    async with aiohttp.ClientSession() as session:
        session.headers.update(headers)
        async with session.get(f"https://api.huntflow.ru/account/{account_id}/vacancies") as response:
            vacansies = await response.json()
            url = f"https://api.huntflow.ru/account/{account_id}/applicants"
            list_task = []
            for vacansy in vacansies["items"]:
                task = asyncio.create_task(async_get_list(url, vacansy["id"]))
                list_task.append(task)

            for i in list_task:
                # ждём чтобы завершились все корутины для измерения времени
                await i


def sync_get():
    session = Session()
    session.headers.update(headers)
    vacancies = session.get(f"https://api.huntflow.ru/account/{account_id}/vacancies").json()
    url = f"https://api.huntflow.ru/account/{account_id}/applicants"
    for vacansy in vacancies["items"]:
        print("sync id=", vacansy["id"])
        session.get(url, params={"vacancy": vacansy["id"]}).json()


@router.get("/parse", response_model=None)
async def parse(access=Depends(UserCRUD.get_current_active_user)):

    async_start_time = time()
    await async_get()
    async_end_time = time()

    sync_start_time = time()
    sync_get()
    sync_end_time = time()

    print("88888888888888888888888888888888888888888888888888888888888888")
    print("async task = ", async_end_time - async_start_time, ", sync task = ", sync_end_time - sync_start_time)
    return None
