from logging import getLogger
from vk_api.vk_api import VkApiMethod
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from .msg_reactions import Spam

logger = getLogger(__name__)


def send_message(vk: VkApiMethod, user_id: int, message: str = "", **kwargs):
    logger.debug(f"Message to {user_id}: {message}")
    params = {"user_id": user_id, "random_id": get_random_id(), "message": message}
    vk.messages.send(**params, **kwargs)


def on_start_message_button(vk, user_id: int, message: str, button_txt: str):
    kb_start = VkKeyboard(one_time=False, inline=True)
    kb_start.add_button(button_txt, color=VkKeyboardColor.POSITIVE)
    send_message(vk, user_id, message=message, keyboard=kb_start.get_keyboard())
