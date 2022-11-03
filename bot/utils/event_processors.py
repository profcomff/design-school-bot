import requests
import bot.schemas.models as schemas
from vk_api.longpoll import Event, VkEventType
from vk_api.vk_api import VkApiMethod
from bot.config import get_settings
from logging import getLogger
import bot.utils.msg_utils as utils
import bot.utils.msg_reactions as reactions


settings = get_settings()


def process_spam(vk: VkApiMethod, event: Event, **kwargs):
    if event.text == reactions.Start.START_BUTTON:
        utils.on_start_message_button(
            vk,
            event.user_id,
            reactions.Spam.START_MESSAGE,
            button_txt=reactions.Spam.START_BUTTON,
        )
    if event.text == reactions.Spam.START_MESSAGE:
        requests.post(
            f"{get_settings().BACKEND_URL}/spam",
            schemas.SpamPost(social_web_id=event.user_id).json(),
        )
        utils.send_message(
            vk, event.user_id, message=reactions.Spam.START_REPLY, **kwargs
        )


def process_registry(vk: VkApiMethod, event: Event, **kwargs):
    if event.text == settings.REGISTRY_MODE:
        users: list[schemas.SpamGet] = requests.get(
            f"{settings.BACKEND_URL}/spam"
        ).json()
        for user in users:
            utils.on_start_message_button(
                vk,
                user.id,
                message=reactions.Registry.START_MESSAGE,
                button_txt=reactions.Registry.START_BUTTON,
            )


def process_workflow(vk: VkApiMethod, event: Event, **kwargs):
    pass


def process_summary(vk: VkApiMethod, event: Event, **kwargs):
    pass
