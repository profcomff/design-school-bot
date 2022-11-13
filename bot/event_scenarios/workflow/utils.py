import requests
from bot.config import get_settings
from bot.event_scenarios.auth import auth_headers

settings = get_settings()


def get_user_db_id(social_web_id: int) -> int:
    res = requests.get(f"{settings.BACKEND_URL}/user/", headers=auth_headers)
    db_user_id = 0
    for user in res.json():
        if int(user["social_web_id"]) == social_web_id:
            db_user_id = user["id"]
    return db_user_id
