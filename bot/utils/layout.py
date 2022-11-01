from vk_api.longpoll import Event, VkEventType
from vk_api.vk_api import VkApiMethod
from logging import getLogger
from msg_reactions import send_message

logger = getLogger(__name__)


def process_event(vk: VkApiMethod, event: Event, **kwargs):
    if event.type == VkEventType.MESSAGE_NEW and event.from_user:
        logger.debug(f"processing message from {event.user_id}: {event.text}")
        send_message(vk, event.user_id, **kwargs)
