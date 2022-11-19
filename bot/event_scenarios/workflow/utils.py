import requests
from bot.config import get_settings
from bot.event_scenarios.auth import auth_headers
from logging import getLogger
from bot.schemas.models import VideoGet
from redis.client import Redis

settings = get_settings()
logger = getLogger(__name__)


def get_user_db_id(social_web_id: int) -> int:
    res = requests.get(f"{settings.BACKEND_URL}/user/", headers=auth_headers)
    if res.status_code != 200:
        logger.critical(f"Unable to get user_id from api: {res.status_code}")
    db_user_id = 0
    for user in res.json():
        if int(user["social_web_id"]) == social_web_id:
            db_user_id = user["id"]
    return db_user_id


def get_video_message(db_user_id: int) -> dict[str, str | None]:
    video = requests.get(
        f"{settings.BACKEND_URL}/uservideo/{db_user_id}", headers=auth_headers
    ).json()
    link = video["link"]
    desc = video["request"]
    return {
        "body": f"{link}\n{desc}",
        "ans_type": video["request_type"],
        "id": video["id"],
    }


def post_solution_to_api(video_id: int, db_user_id: int, type: str = "none", body: dict = None) -> int:
    logger.info(f"post to API: {video_id}, {db_user_id}, {type}")
    if not body:
        res = requests.post(
            f"{settings.BACKEND_URL}/video/{video_id}/response/{db_user_id}/{type}",
            headers=auth_headers,
        )
    else:
        res = requests.post(
            f"{settings.BACKEND_URL}/video/{video_id}/response/{db_user_id}/{type}",
            headers=auth_headers, json=body
        )
    return res.status_code
