import requests
import bot.schemas.models as schemas
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from bot.config import get_settings
import bot.event_scenarios.msg_utils as utils
import bot.event_scenarios.msg_reactions as reactions
import bot.event_scenarios.spam as spam
import bot.event_scenarios.registry as registry


settings = get_settings()


def process_spam(vk: VkApiMethod, event: Event, **kwargs):
    if event.text == reactions.Start.START_BUTTON:
        spam.on_mode_change(vk, event)
    if event.text == reactions.Spam.START_MESSAGE:
        spam.on_start_message(vk, event, **kwargs)


def process_registry(vk: VkApiMethod, event: Event, **kwargs):
    if event.text == settings.REGISTRY_MODE:
        registry.on_mode_change(vk)
    if event.text == reactions.Registry.START_BUTTON:
        registry.on_registration_flow(vk, event, **kwargs)


def process_workflow(vk: VkApiMethod, event: Event, **kwargs):
    pass


def process_summary(vk: VkApiMethod, event: Event, **kwargs):
    pass
