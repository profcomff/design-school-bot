import redis
import bot.schemas.models as schemas
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from bot.config import get_settings
import bot.event_scenarios.msg_reactions as reactions
import bot.event_scenarios.spam as spam
import bot.event_scenarios.registry as registry
import bot.event_scenarios.workflow as workflow
import bot.event_scenarios.summary as summary
import re

settings = get_settings()


def process_spam(vk: VkApiMethod, event: Event, **kwargs):
    if event.text == reactions.Start.START_BUTTON:
        spam.on_mode_change(vk, event)
    if event.text == reactions.Spam.START_BUTTON:
        spam.on_start_message(vk, event, **kwargs)


def process_registry(vk: VkApiMethod, event: Event):
    redis_db = redis.Redis.from_url(settings.REDIS_DSN)
    if event.text == "Начать":
        registry.on_start_button(vk, event)
    if event.text == settings.REGISTRY_MODE:
        registry.on_mode_change(vk)
    elif (
        len(event.text.split()) >= 2
        and event.text.split()[0] == settings.REGISTRY_MODE
        and event.text.split()[1] == "spam_message"
    ):
        message = event.text.split(" spam_message ")[-1]
        if settings.REGISTRY_MODE not in message:
            registry.on_spam_message(vk, message)
    elif event.text == reactions.Registry.START_BUTTON:
        registry.on_start_button(vk, event)
    elif re.match(r"([А-ЯЁ][а-яё]+[\-\s]?){2,}", event.text):
        # username received
        registry.on_fio_ans(vk, event)

    elif redis_db.hget(event.user_id, "name") and re.match(r"\d{7}", event.text):
        # union number received
        registry.on_union_ans(vk, event)

    elif redis_db.hget(event.user_id, "union_num") and event.text in [
        y.value for y in schemas.Year
    ]:
        # year received
        registry.on_year_ans(vk, event)

    elif redis_db.hget(event.user_id, "year") and event.text in [
        d.name for d in registry.get_directions()
    ]:
        # direction received
        registry.on_direction_ans(vk, event)

    elif redis_db.hget(event.user_id, "direction_id") and event.text in [
        reactions.Registry.APPROVE_TRUE,
        reactions.Registry.APPROVE_FALSE,
    ]:
        # on approve / discard
        registry.on_approve(vk, event)

    elif redis_db.hget(event.user_id, "approved") and not redis_db.hexists(
        event.user_id, "registrated"
    ):
        # user cv received
        registry.on_about(vk, event)
    elif event.text != "Начать" and redis_db.hexists(event.user_id, "registrated"):
        registry.on_random_end(vk, event)
    elif (
        event.text != "Начать"
        and not redis_db.hexists(event.user_id, "registrated")
        and not redis_db.hexists(event.user_id, "start_button")
    ):
        registry.on_random_begin(vk, event)


def process_workflow(vk: VkApiMethod, event: Event):
    redis_db = redis.Redis.from_url(settings.REDIS_DSN)
    if event.text == settings.WORKFLOW_MODE:
        return None
    elif event.text == f"{settings.WORKFLOW_MODE} send_message":
        workflow.on_mode_change(vk)
    elif event.text == reactions.Workflow.CONFIRM_BUTTON:
        workflow.on_start_button(vk, event)
    elif (
        event.text
        and redis_db.hexists(event.user_id, "workflow_type")
        and redis_db.hget(event.user_id, "workflow_type").decode("utf-8") == "end"
    ):
        workflow.on_random_message(vk, event)
    elif event.text == "Начать" or event.text == reactions.Registry.START_BUTTON:
        workflow.on_registry_expiry(vk, event)


    elif (
        redis_db.hexists(event.user_id, "workflow")
        and redis_db.hexists(event.user_id, "workflow_type")
        and redis_db.hget(event.user_id, "workflow_type").decode("utf-8") == "none"
        and event.text == reactions.Workflow.NEXT_VIDEO_BUTTON
    ):
        workflow.on_none_request_ans(vk, event)
    elif (
        redis_db.hexists(event.user_id, "workflow")
        and redis_db.hexists(event.user_id, "workflow_type")
        and redis_db.hget(event.user_id, "workflow_type").decode("utf-8")
        == "end_course"
        and event.text == reactions.Workflow.COOL_BUTTON
    ):
        workflow.on_end_course(vk, event)
    elif (
        event.text != f"{settings.WORKFLOW_MODE} send_message"
        and redis_db.hexists(event.user_id, "workflow")
        and redis_db.hget(event.user_id, "workflow").decode("utf-8") == "on workflow"
    ):
        workflow.on_solution_received(vk, event)
    elif (
        event.text
        and event.text != reactions.Workflow.NEXT_VIDEO_BUTTON
        and redis_db.hexists(event.user_id, "workflow")
        and redis_db.hget(event.user_id, "workflow").decode("utf-8") == "solved"
    ):
        workflow.on_approve(vk, event)
    elif (
        event.text == reactions.Workflow.NEXT_VIDEO_BUTTON
        and redis_db.hexists(event.user_id, "workflow")
        and redis_db.hget(event.user_id, "workflow").decode("utf-8") == "approved"
    ):
        workflow.on_start_button(vk, event)


def process_summary(vk: VkApiMethod, event: Event):
    pass
