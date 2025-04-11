from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from app.crud import get_comments, get_comments_by_news_id, add_comment, delete_comment

router = APIRouter(prefix='/comments')

@router.get("", response_model=List[dict])
async def app_get_comments():
    comments_data = await get_comments()

    return JSONResponse({"comments_data": comments_data, "status": True}, status_code=200)

@router.get("/{news_id}", response_model=List[dict])
async def app_get_comments_by_news_id(news_id: int):
    comments_data = await get_comments_by_news_id(news_id)

    if not comments_data:
        return JSONResponse({"status": False}, status_code=404)
    else:
        return JSONResponse({"comments_data": comments_data, "status": True}, status_code=200)

@router.post("/add", response_model=List[dict])
async def app_add_comment(comment_data: dict):
    comment_id = await add_comment(comment_data)

    return JSONResponse({"comment_id": comment_id, "status": True}, status_code=201)

@router.delete("/{comment_id}", response_model=List[dict])
async def app_delete_comment(comment_id: int):
    comment_id = await delete_comment(comment_id)

    if not comment_id:
        return JSONResponse({"status": False}, status_code=404)
    else:
        return JSONResponse({"comment_id": comment_id, "status": True}, status_code=200)