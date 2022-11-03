import requests
import bot.schemas.models as schemas
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from bot.config import get_settings
from logging import getLogger
import bot.event_scenarios.msg_utils as utils
import bot.event_scenarios.msg_reactions as reactions
from .utils import RegistrationQuery

settings = get_settings()


def on_mode_change(vk: VkApiMethod) -> None:
    """on 'register_mode' code bot sends messages to registrate"""
    # users: list[schemas.SpamGet] = requests.get(
    # f"{settings.BACKEND_URL}/spam"
    # ).json()

    users = [236941574]
    for user in users:
        utils.on_start_message_button(
            vk,
            user,
            message=reactions.Registry.START_MESSAGE,
            button_txt=reactions.Registry.START_BUTTON,
        )


def on_registration_flow(vk: VkApiMethod, event: Event, **kwargs):
    pass
