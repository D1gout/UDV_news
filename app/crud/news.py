from datetime import datetime

from app.json_func import load_json, save_json


async def get_news_list():
    news_data = await load_json('news.json')
    comments_data = await load_json('comments.json')

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

    return {
        "news": filtered_news,
        "news_count": len(filtered_news)
    }

async def get_news_by_id(news_id):
    news_data = await load_json('news.json')
    comments_data = await load_json('comments.json')

    news_item = next((n for n in news_data["news"] if n["id"] == news_id), None)

    if not news_item or news_item.get("deleted", False):
        return False

    comments = [c for c in comments_data["comments"] if c["news_id"] == news_id]

    return {
        **news_item,
        "comments": comments,
        "comments_count": len(comments)
    }

async def add_news(news_data):
    all_news_data = await load_json('news.json')

    new_id = max([news["id"] for news in all_news_data["news"]]) + 1

    all_news_data["news"].append({
        "id": new_id,
        "title": news_data["title"],
        "date": datetime.now().replace(microsecond=0).isoformat(),
        "body": news_data["body"],
        "deleted": False
    })

    if "news_count" in all_news_data:
        all_news_data["news_count"] += 1
    else:
        all_news_data["news_count"] = len(all_news_data["news"])

    await save_json('news.json', all_news_data)

    return new_id

async def delete_news(news_id):
    all_news_data = await load_json('news.json')

    news_item = next((n for n in all_news_data["news"] if n["id"] == news_id), None)

    if not news_item:
        return False

    news_item["deleted"] = True

    await save_json('news.json', all_news_data)

    return news_item['id']