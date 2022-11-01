from logging import getLogger
from vk_api.vk_api import VkApiMethod
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

logger = getLogger(__name__)


def send_message(vk: VkApiMethod, user_id: int, message: str, **kwargs):
    logger.debug(f"Message to {user_id}: {message}")
    params = {"user_id": user_id, "random_id": get_random_id(), "message": message}
    vk.messages.send(**params, **kwargs)


def on_start_message(vk):
    send_message()
