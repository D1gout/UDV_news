from datetime import datetime

from app.crud import load_json
from app.json_func import save_json


async def get_comments():
    comments_data = await load_json('comments.json')

    comments_by_news = {}
    for comment in comments_data["comments"]:
        news_id = comment["news_id"]
        cleaned_comment = {k: v for k, v in comment.items() if k != "news_id"}
        comments_by_news.setdefault(news_id, []).append(cleaned_comment)

    return {
        "comments": comments_by_news,
        "comments_count": sum(len(comments) for comments in comments_by_news.values())
    }

async def get_comments_by_news_id(news_id):
    comments_data = await load_json('comments.json')

    comments = [comment for comment in comments_data["comments"] if comment["news_id"] == news_id]

    return {
        "comments": comments,
        "comments_count": len(comments)
    }

async def add_comment(comment_data):
    all_comments_data = await load_json('comments.json')

    new_id = max([comment["id"] for comment in all_comments_data["comments"]]) + 1

    all_comments_data["comments"].append({
        "id": new_id,
        "news_id": comment_data["news_id"],
        "title": comment_data["title"],
        "date": datetime.now().replace(microsecond=0).isoformat(),
        "comment": comment_data["comment"],
    })

    if "comments_count" in all_comments_data:
        all_comments_data["comments_count"] += 1
    else:
        all_comments_data["comments_count"] = len(all_comments_data["comments"])

    await save_json('comments.json', all_comments_data)

    return new_id

async def delete_comment(comment_id):
    all_comments_data = await load_json('comments.json')

    comment_to_delete = next((c for c in all_comments_data["comments"] if c["id"] == comment_id), None)

    if not comment_to_delete:
        return False

    all_comments_data["comments"].remove(comment_to_delete)

    if "comments_count" in all_comments_data:
        all_comments_data["comments_count"] -= 1
    else:
        all_comments_data["comments_count"] = len(all_comments_data["comments"])

    await save_json('comments.json', all_comments_data)

    return comment_id