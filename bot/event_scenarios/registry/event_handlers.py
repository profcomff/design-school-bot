import requests
import bot.schemas.models as schemas
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from bot.config import get_settings
from logging import getLogger
import bot.event_scenarios.msg_utils as utils
import bot.event_scenarios.msg_reactions as reactions
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from .utils import Name

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


def on_start_button(vk: VkApiMethod, event: Event) -> None:
    utils.send_message(vk, event.user_id, message=reactions.Registry.FIO_QUESTION)


def on_fio_ans(vk: VkApiMethod, event: Event):
    name = Name(event.text)
    if name.is_valid():
        utils.send_message(vk, event.user_id, message=reactions.Registry.UNION_QUESTION)
    else:
        utils.send_message(vk, event.user_id, message=reactions.Registry.ON_FAILURE)


def on_union_ans(vk: VkApiMethod, event: Event) -> None:
    utils.send_message(vk, event.user_id, message=reactions.Registry.YEAR_QUESTION)


def on_year_ans(vk: VkApiMethod, event: Event) -> None:
    utils.send_message(vk, event.user_id, message=reactions.Registry.DIRECTION_QUESTION)


def on_direction_ans(vk: VkApiMethod, event: Event, **kwargs):
    kb = VkKeyboard(one_time=False, inline=True)
    for direction in schemas.Directions:
        kb.add_button(direction.value, color=VkKeyboardColor.SECONDARY)
    utils.send_message(vk, event.user_id,
                       message=reactions.Registry.DIRECTION_BUTTON_MESSAGE,
                       keyboard=kb.get_keyboard(), **kwargs)


def on_approve(vk: VkApiMethod, event: Event):
    pass
