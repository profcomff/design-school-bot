import bot.event_scenarios.msg_reactions as reactions
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bot.config import get_settings
import bot.event_scenarios.msg_utils as utils
from bot.event_scenarios.auth import auth_headers
from .utils import get_user_db_id
import redis
import requests
from textwrap import dedent


settings = get_settings()
redis_db = redis.Redis.from_url(settings.REDIS_DSN)


def on_registry_expiry(vk: VkApiMethod, event: Event):
    utils.send_message(vk, event.user_id, dedent(reactions.Workflow.REGISTRY_EXPIRED))


def on_mode_change(vk: VkApiMethod):
    res = requests.get(f"{settings.BACKEND_URL}/user/", headers=auth_headers)
    users = res.json()
    kb = VkKeyboard(one_time=True, inline=False)
    kb.add_button(reactions.Workflow.CONFIRM_BUTTON, color=VkKeyboardColor.POSITIVE)
    for user in users:
        utils.send_message(
            vk,
            int(user["social_web_id"]),
            message=reactions.Workflow.start_message(user["direction_id"]),
            keyboard=kb.get_keyboard(),
        )


def on_start_button(vk: VkApiMethod, event: Event):
    redis_db.hdel(event.user_id,
                  "workflow",
                  "workflow_type")
    redis_db.hset(event.user_id, "workflow", "started")
    db_user_id = get_user_db_id(event.user_id)
    video = requests.get(
        f"{settings.BACKEND_URL}/uservideo/{db_user_id}", headers=auth_headers
    ).json()
    link = video["link"]
    desc = video["request"]
    utils.send_message(vk, event.user_id, message=f"{link}\n{desc}")
    request_type = video['request_type']
    if request_type is None:
        redis_db.hset(event.user_id, "workflow_type", 'none')
    else:
        redis_db.hset(event.user_id, "workflow_type", request_type)
    redis_db.hset(event.user_id, "workflow", "on workflow")


def on_none_request_ans(vk: VkApiMethod, event: Event):
    utils.send_message(vk, event.user_id, message='null req')
    db_user_id = get_user_db_id(event.user_id)
    video = requests.get(
        f"{settings.BACKEND_URL}/uservideo/{db_user_id}", headers=auth_headers
    ).json()
    request_type = video['request_type']
    if request_type is None:
        redis_db.hset(event.user_id, "workflow_type", 'none')
    else:
        redis_db.hset(event.user_id, "workflow_type", request_type)
    link = video["link"]
    desc = video["request"]
    utils.send_message(vk, event.user_id, message=f"{link}\n{desc}")


def on_text_request_ans(vk: VkApiMethod, event: Event):
    utils.send_message(vk, event.user_id, message='text req')


def on_video_request_ans(vk: VkApiMethod, event: Event):
    utils.send_message(vk, event.user_id, message='video req')


def on_file_request_ans(vk: VkApiMethod, event: Event):
    utils.send_message(vk, event.user_id, message='video req')