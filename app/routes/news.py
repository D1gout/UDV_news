from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from app.json_loader import load_json

router = APIRouter(prefix='/news')


@router.get("/", response_model=List[dict])
async def get_news_list():
    news_data = load_json('news.json')
    comments_data = load_json('comments.json')

    comments_by_news = {}
    for comment in comments_data["comments"]:
        news_id = comment["news_id"]
        comments_by_news.setdefault(news_id, []).append(comment)

    filtered_news = []
    for news in news_data["news"]:
        if not news.get("deleted", False):
            news_copy = news.copy()
            news_copy["comments_count"] = len(comments_by_news.get(news["id"], []))
            filtered_news.append(news_copy)

    return JSONResponse(content={
        "news": filtered_news,
        "news_count": len(filtered_news)
    })


@router.get("/news/{news_id}", response_model=List[dict])
def get_news_by_id(news_id: int):
    news_data = load_json(NEWS_FILE)
    comments_data = load_json(COMMENTS_FILE)

    news_item = next((n for n in news_data["news"] if n["id"] == news_id), None)

    if not news_item or news_item.get("deleted", False):
        raise HTTPException(status_code=404, detail="News not found")

    comments = [c for c in comments_data["comments"] if c["news_id"] == news_id]

    result = {
        **news_item,
        "comments": comments,
        "comments_count": len(comments)
    }

    return JSONResponse(content=result)