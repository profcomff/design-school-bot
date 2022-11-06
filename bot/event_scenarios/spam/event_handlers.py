import requests
import redis
import bot.schemas.models as schemas
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from bot.config import get_settings
import bot.event_scenarios.msg_utils as utils
import bot.event_scenarios.msg_reactions as reactions

settings = get_settings()


def on_mode_change(vk: VkApiMethod, event: Event) -> None:
    utils.on_start_message_button(
        vk,
        event.user_id,
        reactions.Spam.START_MESSAGE,
        button_txt=reactions.Spam.START_BUTTON,
    )


def on_start_message(vk: VkApiMethod, event: Event, **kwargs) -> None:
    requests.post(
        f"{settings.BACKEND_URL}/spam",
        schemas.SpamPost(social_web_id=event.user_id).json(),
    )
    utils.send_message(vk, event.user_id, message=reactions.Spam.START_REPLY, **kwargs)
