import bot.event_scenarios.msg_reactions as reactions
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bot.config import get_settings
import bot.event_scenarios.msg_utils as utils
from bot.event_scenarios.auth import auth_headers
from .utils import get_user_db_id
import redis
import requests
from textwrap import dedent
from logging import getLogger

logger = getLogger(__name__)
settings = get_settings()
redis_db = redis.Redis.from_url(settings.REDIS_DSN)
