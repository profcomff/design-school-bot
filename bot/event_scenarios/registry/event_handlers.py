import requests
import redis
from logging import getLogger
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from bot.config import get_settings
import bot.event_scenarios.msg_utils as utils
import bot.event_scenarios.msg_reactions as reactions
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from .utils import Name, get_directions
from bot.event_scenarios.auth import auth_headers
from textwrap import dedent

settings = get_settings()
redis_db = redis.Redis.from_url(settings.REDIS_DSN)
directions = get_directions()
logger = getLogger(__name__)


def on_random_begin(vk: VkApiMethod, event: Event):
    utils.on_start_message_button(
        vk, event.user_id, message="Привет!", button_txt="Начать"
    )


def on_mode_change(vk: VkApiMethod) -> None:
    """on 'register_mode' code bot sends messages to registrate"""
    users: list = requests.get(
        f"{settings.BACKEND_URL}/spam/", headers=auth_headers
    ).json()
    ids = set()
    for user in users:
        ids.add(int(user.get("social_web_id")))
    for user_id in ids:
        utils.on_start_message_button(
            vk,
            user_id,
            message=reactions.Registry.START_MESSAGE,
            button_txt=reactions.Registry.START_BUTTON,
        )


def on_start_button(vk: VkApiMethod, event: Event) -> None:
    redis_db.hdel(
        event.user_id,
        "name",
        "union_num",
        "year",
        "direction_id",
        "registrated",
        "approved",
        "start_button",
    )
    redis_db.hset(event.user_id, "start_button", "started")
    utils.send_message(vk, event.user_id, message=reactions.Registry.FIO_QUESTION)
    redis_db.hset(name=event.user_id, key="social_web_id", value=event.user_id)


def on_fio_ans(vk: VkApiMethod, event: Event):
    name = Name(event.text)
    if name.is_valid():
        utils.send_message(
            vk, event.user_id, message=dedent(reactions.Registry.UNION_QUESTION)
        )
        redis_db.hset(name=event.user_id, key="name", value=event.text)
    else:
        utils.send_message(vk, event.user_id, message=reactions.Registry.ON_FAILURE)


def on_union_ans(vk: VkApiMethod, event: Event) -> None:
    utils.send_message(
        vk, event.user_id, message=dedent(reactions.Registry.YEAR_QUESTION)
    )
    redis_db.hset(name=event.user_id, key="union_num", value=event.text)


def on_year_ans(vk: VkApiMethod, event: Event) -> None:
    redis_db.hset(name=event.user_id, key="year", value=event.text)
    kb = VkKeyboard(one_time=False, inline=True)

    for i in range(len(directions)):
        kb.add_button(directions[i].name)
        if i + 1 < len(directions):
            kb.add_line()
    utils.send_message(
        vk,
        event.user_id,
        message=dedent(reactions.Registry.DIRECTION_QUESTION),
        keyboard=kb.get_keyboard(),
        attach=None,
    )


def on_discard_direction(vk: VkApiMethod, event: Event):
    kb = VkKeyboard(one_time=False, inline=True)

    for i in range(len(directions)):
        kb.add_button(directions[i].name)
        if i + 1 < len(directions):
            kb.add_line()
    utils.send_message(
        vk,
        event.user_id,
        message=dedent(reactions.Registry.DIRECTION_QUESTION),
        keyboard=kb.get_keyboard(),
        attach=None,
    )


def on_direction_ans(vk: VkApiMethod, event: Event):
    db_id = 1
    for d in directions:
        if d.name == event.text:
            db_id = d.db_id
    redis_db.hset(name=event.user_id, key="direction_id", value=db_id)
    kb = VkKeyboard(one_time=False, inline=True)
    kb.add_button(reactions.Registry.APPROVE_TRUE, color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button(reactions.Registry.APPROVE_FALSE, color=VkKeyboardColor.NEGATIVE)
    utils.send_message(
        vk,
        event.user_id,
        message=reactions.Registry.APPROVE_QUESTION,
        keyboard=kb.get_keyboard(),
    )


def on_approve(vk: VkApiMethod, event: Event):
    if event.text == reactions.Registry.APPROVE_TRUE:
        utils.send_message(
            vk, event.user_id, message=dedent(reactions.Registry.ABOUT_QUESTION)
        )
        redis_db.hset(event.user_id, "approved", "approved")
    if event.text == reactions.Registry.APPROVE_FALSE:
        utils.send_message(vk, event.user_id, message="Ладно, давай снова:")
        redis_db.hdel(event.user_id, "direction_id")
        on_discard_direction(vk, event)


def on_about(vk: VkApiMethod, event: Event):

    redis_db.hset(name=event.user_id, key="registrated", value="registrated")
    # post user data to backend
    register_data = redis_db.hgetall(event.user_id)
    fio = register_data[b"name"].decode("utf-8").split()
    if len(fio) == 3:
        middle_name = fio[2]
    elif len(fio) == 2:
        middle_name = ""
    user = dict(
        union_id=register_data[b"union_num"].decode("utf-8"),
        direction_id=register_data[b"direction_id"].decode("utf-8"),
        first_name=fio[1],
        last_name=fio[0],
        middle_name=middle_name,
        year=register_data[b"year"].decode("utf-8"),
        readme=event.text,
        social_web_id=register_data[b"social_web_id"].decode("utf-8"),
    )
    res = requests.post(
        f"{settings.BACKEND_URL}/user/", json=user, headers=auth_headers
    )
    if res.status_code == 200:
        utils.send_message(
            vk, event.user_id, message=dedent(reactions.Registry.ON_CV_ANSWER)
        )
    elif res.status_code == 409:
        utils.send_message(
            vk,
            event.user_id,
            message=dedent(
                "Вы уже в базе данных. Для изменения данных обратитесь в поддержку"
            ),
        )
    else:
        utils.send_message(vk, event.user_id, message="Something went wrong")
    logger.info(f"{res.status_code}-{register_data[b'social_web_id'].decode('utf-8')}")


def on_random_end(vk: VkApiMethod, event: Event):
    utils.send_message(
        vk,
        event.user_id,
        message="Ты уже зарегистрировался, мы сообщим о начале учебы!",
    )


def on_spam_message(vk: VkApiMethod, message):
    res = requests.get(f"{settings.BACKEND_URL}/user/", headers=auth_headers)
    users = res.json()
    for user in users:
        utils.send_message(
            vk,
            int(user["social_web_id"]),
            message=message,
        )
