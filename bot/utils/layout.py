from bot.config import get_settings
from vk_api.longpoll import Event, VkEventType
from vk_api.vk_api import VkApiMethod
from logging import getLogger

import bot.utils.msg_utils as utils
import bot.utils.msg_reactions as reactions
from bot.utils.mode import change_mode

from bot.utils.mode import Mode
import bot.utils.event_processors as processor

logger = getLogger(__name__)
settings = get_settings()


def process_event(vk: VkApiMethod, event: Event, **kwargs):
    if event.type == VkEventType.MESSAGE_NEW and event.from_user:
        logger.info(f"processing message from {event.user_id}: {event.text}")
        if change_mode(event.text):
            utils.send_message(
                vk, event.user_id, message=change_mode(event.text), **kwargs
            )
        if settings.CURRENT_MODE == Mode.spam:
            processor.process_spam(vk, event, **kwargs)
        elif settings.CURRENT_MODE == Mode.registry:
            processor.process_registry(vk, event, **kwargs)
        elif settings.CURRENT_MODE == Mode.workflow:
            processor.process_workflow(vk, event, **kwargs)
        elif settings.CURRENT_MODE == Mode.summary:
            processor.process_summary(vk, event, **kwargs)
