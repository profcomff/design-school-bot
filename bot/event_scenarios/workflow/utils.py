import requests
from bot.config import get_settings
from bot.event_scenarios.auth import auth_headers
from logging import getLogger
import bot.event_scenarios.msg_reactions as reactions
import time

settings = get_settings()
logger = getLogger(__name__)
MAX_RETRIES = 5
retries = 0


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
    res = requests.get(
        f"{settings.BACKEND_URL}/uservideo/{db_user_id}", headers=auth_headers
    )
    if res.status_code == 200 and res.text == "Course ended":
        return {
            "body": reactions.Workflow.COURSE_ENDED,
            "ans_type": "end_course",
            "id": 0,
        }
    video = res.json()
    link = video["link"]
    desc = video["request"]
    return {
        "body": f"{link}\n{desc}",
        "ans_type": video["request_type"],
        "id": video["id"],
    }


def post_until_success(retries=5, timeout_ms: float = 500, fail_code: int = 500):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            curr_timeout_ms = timeout_ms
            while attempt < retries:
                code = func(*args, **kwargs)
                if code != fail_code:
                    return code
                else:
                    logger.info(f"Retrying... {attempt}")
                    time.sleep(curr_timeout_ms / 1000)
                    attempt += 1
                    curr_timeout_ms *= 2
            return code
        return wrapper
    return decorator


@post_until_success()
def post_solution_to_api(
        video_id: int, db_user_id: int, type: str = "none", body: dict = None
) -> int:
    logger.info(f"post to API: {video_id}, {db_user_id}, {type}")
    if not body:
        res = requests.post(
            f"{settings.BACKEND_URL}/video/{video_id}/response/{db_user_id}/{type}",
            headers=auth_headers,
        )
    else:
        if type == "file":
            type = "text"

        res = requests.post(
            f"{settings.BACKEND_URL}/video/{video_id}/response/{db_user_id}/{type}",
            headers=auth_headers,
            json=body,
        )
    return res.status_code
