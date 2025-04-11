from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from app.crud import get_news_list, get_news_by_id, add_news, delete_news

router = APIRouter(prefix='/news')


@router.get("", response_model=List[dict])
async def app_get_news_list():
    all_news_data = await get_news_list()

    return JSONResponse({"all_news_data": all_news_data, 'status': True}, status_code=200)


@router.get("/{news_id}", response_model=List[dict])
async def app_get_news_by_id(news_id: int):
    news_data = await get_news_by_id(news_id)

    if not news_data:
        return JSONResponse({"status": False}, status_code=404)
    else:
        return JSONResponse({"news_data": news_data, 'status': True}, status_code=200)


# Добавление новости
@router.post("/add", response_model=List[dict])
async def app_add_news(news_data: dict):
    news_id = await add_news(news_data)

    return JSONResponse({"news_id": news_id, "status": True}, status_code=201)

# Удаление новости
@router.delete("/{news_id}", response_model=List[dict])
async def app_delete_news(news_id: int):
    news_id = await delete_news(news_id)

    if not news_id:
        return JSONResponse({"status": False}, status_code=404)
    else:
        return JSONResponse({"news_id": news_id, 'status': True}, status_code=200)