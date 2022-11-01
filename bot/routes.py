import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import get_settings


vk_session = vk_api.VkApi(token=get_settings().TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
