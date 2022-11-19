import requests
import redis
from logging import getLogger
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from bot.config import get_settings
import bot.event_scenarios.msg_utils as utils
import bot.event_scenarios.msg_reactions as reactions
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bot.event_scenarios.auth import auth_headers
from textwrap import dedent
