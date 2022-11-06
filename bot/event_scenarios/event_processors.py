import requests
import redis
import bot.schemas.models as schemas
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from bot.config import get_settings
import bot.event_scenarios.msg_reactions as reactions
import bot.event_scenarios.spam as spam
import bot.event_scenarios.registry as registry
import re


settings = get_settings()


class RedisUser:
    union_id: str
    direction_id: int
    first_name: str
    middle_name: str
    last_name: str
    year: str
    readme: str


def redis_model_completed(model: dict[str, int | str]) -> bool:
    for row in [*RedisUser.__dict__.keys(), "social_web_id"]:
        if row not in model.keys():
            return False
    return True


def process_spam(vk: VkApiMethod, event: Event, **kwargs):
    if event.text == reactions.Start.START_BUTTON:
        spam.on_mode_change(vk, event)
    if event.text == reactions.Spam.START_BUTTON:
        spam.on_start_message(vk, event, **kwargs)


def process_registry(vk: VkApiMethod, event: Event, **kwargs):
    redis_db = redis.Redis.from_url(settings.REDIS_DSN)
    if event.text == settings.REGISTRY_MODE:
        registry.on_mode_change(vk)
    elif event.text == reactions.Registry.START_BUTTON:
        registry.on_start_button(vk, event)
    elif re.match(r"([А-ЯЁ][а-яё]+[\-\s]?){3,}", event.text):
        # username received
        registry.on_fio_ans(vk, event)

    elif redis_db.hget(event.user_id, "name") and re.match(r"\d{7}", event.text):
        # union number received
        registry.on_union_ans(vk, event)

    elif redis_db.hget(event.user_id, "union_num") and event.text in [
        y.value for y in schemas.Year
    ]:
        # year received
        registry.on_year_ans(vk, event)

    elif redis_db.hget(event.user_id, "year") and event.text in [
        d.name for d in registry.get_directions()
    ]:
        # direction received
        registry.on_direction_ans(vk, event)

    elif redis_db.hget(event.user_id, "direction_id") and event.text in [
        reactions.Registry.APPROVE_TRUE,
        reactions.Registry.APPROVE_FALSE,
    ]:
        # on approve / discard
        registry.on_approve(vk, event)

    elif redis_db.hget(event.user_id, "approved") and not redis_db.hexists(
        event.user_id, "registrated"
    ):
        # user cv received
        registry.on_about(vk, event)


def process_workflow(vk: VkApiMethod, event: Event, **kwargs):
    pass


def process_summary(vk: VkApiMethod, event: Event, **kwargs):
    pass
