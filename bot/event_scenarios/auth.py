import json
import requests
from bot.config import get_settings


def _auth_headers():
    settings = get_settings()
    beaver = requests.post(
        f"{settings.BACKEND_URL}/token",
        {"username": settings.BACKEND_USER, "password": settings.BACKEND_PASSWORD},
    )
    auth_data = json.loads(beaver.content)
    return {"Authorization": f"Bearer {auth_data.get('access_token')}"}


auth_headers = _auth_headers()
