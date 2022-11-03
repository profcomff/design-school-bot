import requests
from bot.schemas.models import SpamPost
from vk_api.longpoll import Event, VkEventType
from vk_api.vk_api import VkApiMethod
from bot.config import get_settings
from logging import getLogger
import bot.utils.msg_utils as utils
import bot.utils.msg_reactions as reactions
from .mode import change_mode

logger = getLogger(__name__)
settings = get_settings()


def process_spam(vk: VkApiMethod, event: Event, **kwargs):
    logger.debug(f"processing message from {event.user_id}: {event.text}")
    if event.text == reactions.Start.start_button:
        utils.on_start_message(vk, event.user_id)
    if event.text == reactions.Registry.start_message:
        # requests.post(f"{get_settings().BACKEND_URL}/spam",
        #              SpamPost(social_web_id=event.user_id).json())
        utils.send_message(vk, event.user_id, message=reactions.Registry.start_reply, **kwargs)


def process_registry(vk: VkApiMethod, event: Event, **kwargs):
    pass


def process_workflow(vk: VkApiMethod, event: Event, **kwargs):
    pass


def process_summary(vk: VkApiMethod, event: Event, **kwargs):
    pass
