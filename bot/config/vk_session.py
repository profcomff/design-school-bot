import vk_api
from vk_api.longpoll import VkLongPoll
from .settings import get_settings


vk_session = vk_api.VkApi(token=get_settings().TOKEN, api_version="5.131")
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
