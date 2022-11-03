from logging import getLogger
from vk_api.vk_api import VkApiMethod
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from .msg_reactions import Registry
logger = getLogger(__name__)


def send_message(vk: VkApiMethod, user_id: int, message: str = "", **kwargs):
    logger.debug(f"Message to {user_id}: {message}")
    params = {"user_id": user_id, "random_id": get_random_id(), "message": message}
    vk.messages.send(**params, **kwargs)


def on_start_message(vk, user_id: int):
    start_message = Registry.start_message
    kb_start = VkKeyboard(one_time=False, inline=True)
    kb_start.add_button(start_message, color=VkKeyboardColor.POSITIVE)
    send_message(vk, user_id, message="Привет!", keyboard=kb_start.get_keyboard())
