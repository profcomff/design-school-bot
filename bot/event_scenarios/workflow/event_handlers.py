import bot.event_scenarios.msg_reactions as reactions
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bot.config import get_settings
import bot.event_scenarios.msg_utils as utils
from bot.event_scenarios.auth import auth_headers
from .utils import get_user_db_id, get_video_message, post_solution_to_api
import redis
import requests
from textwrap import dedent
from logging import getLogger

logger = getLogger(__name__)
settings = get_settings()
redis_db = redis.Redis.from_url(settings.REDIS_DSN)


def on_registry_expiry(vk: VkApiMethod, event: Event):
    utils.send_message(vk, event.user_id, dedent(reactions.Workflow.REGISTRY_EXPIRED))


def on_mode_change(vk: VkApiMethod):
    res = requests.get(f"{settings.BACKEND_URL}/user/", headers=auth_headers)
    if res.status_code != 200:
        logger.critical(f"Unable to get users: {res.status_code}")
    users = res.json()
    kb = VkKeyboard(one_time=True, inline=False)
    kb.add_button(reactions.Workflow.CONFIRM_BUTTON, color=VkKeyboardColor.POSITIVE)
    for user in users:
        utils.send_message(
            vk,
            int(user["social_web_id"]),
            message=reactions.Workflow.start_message(user["direction_id"]),
            keyboard=kb.get_keyboard(),
        )


def on_start_button(vk: VkApiMethod, event: Event):
    redis_db.hdel(event.user_id, "workflow", "workflow_type")
    redis_db.hset(event.user_id, "workflow", "started")
    send_video_task(vk, event)


def send_video_task(vk: VkApiMethod, event: Event):
    db_user_id = get_user_db_id(event.user_id)
    video = get_video_message(db_user_id)
    ans_type = video["ans_type"]
    if ans_type == "end_course":
        redis_db.hset(event.user_id, "workflow_type", ans_type)
        kb = VkKeyboard(one_time=False, inline=True)
        kb.add_button(reactions.Workflow.COOL_BUTTON, color=VkKeyboardColor.POSITIVE)
        utils.send_message(
            vk, event.user_id, message=video["body"], keyboard=kb.get_keyboard()
        )
        return None
    redis_db.hset(event.user_id, "video_id", video["id"])
    if ans_type is None:
        redis_db.hset(event.user_id, "workflow_type", "none")
        redis_db.hset(event.user_id, "video_type", "none")
        kb = VkKeyboard(one_time=False, inline=True)
        kb.add_button(
            reactions.Workflow.NEXT_VIDEO_BUTTON, color=VkKeyboardColor.POSITIVE
        )
        utils.send_message(
            vk, event.user_id, message=video["body"], keyboard=kb.get_keyboard()
        )
    else:
        redis_db.hset(event.user_id, "video_type", ans_type)
        redis_db.hset(event.user_id, "workflow_type", ans_type)
        utils.send_message(
            vk, event.user_id, message=video["body"]
        )
    redis_db.hset(event.user_id, "workflow", "on workflow")


def on_none_request_ans(vk: VkApiMethod, event: Event):
    commit_solution(event)
    send_video_task(vk, event)


def on_approve(vk: VkApiMethod, event: Event):
    if event.text == reactions.Workflow.APPROVE_TRUE:
        redis_db.hset(event.user_id, "workflow", "approved")
        api_res = commit_solution(event)
        if api_res != 200:
            utils.send_message(
                vk,
                event.user_id,
                message=dedent("????????????. ????????????????, ???????????? ???? ???? google drive/google docs ?????? ?????? ???????????????????? ??????????????"))
        kb = VkKeyboard(one_time=False, inline=True)
        kb.add_button(
            reactions.Workflow.NEXT_VIDEO_BUTTON, color=VkKeyboardColor.POSITIVE
        )
        utils.send_message(
            vk,
            event.user_id,
            message=reactions.Workflow.ON_APPROVE_TRUE_ANS,
            keyboard=kb.get_keyboard(),
        )
    if event.text == reactions.Workflow.APPROVE_FALSE:
        redis_db.hset(event.user_id, "workflow", "on workflow")
        redis_db.hdel(event.user_id, "content")
        utils.send_message(
            vk, event.user_id, message=reactions.Workflow.ON_APPROVE_FALSE_ANS
        )


def on_solution_received(vk: VkApiMethod, event: Event):
    redis_db.hset(event.user_id, "workflow", "solved")
    redis_db.hset(event.user_id, "content", event.text)
    kb = VkKeyboard(one_time=False, inline=True)
    kb.add_button(reactions.Workflow.APPROVE_TRUE, color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button(reactions.Workflow.APPROVE_FALSE, color=VkKeyboardColor.NEGATIVE)
    utils.send_message(
        vk,
        event.user_id,
        message=reactions.Workflow.APPROVE_QUESTION,
        keyboard=kb.get_keyboard(),
    )


def on_end_course(vk: VkApiMethod, event: Event):
    redis_db.hset(event.user_id, "workflow_type", "end")
    direction_id = int(redis_db.hgetall(event.user_id)[b"direction_id"].decode("utf-8"))
    utils.send_message(vk, event.user_id, message=reactions.Workflow.end_course_message(direction_id))


def on_random_message(vk: VkApiMethod, event: Event):
    utils.send_message(vk, event.user_id, message=reactions.Workflow.ON_ENDED_RANDOM)


def commit_solution(event: Event):
    video_id = int(redis_db.hget(event.user_id, "video_id").decode("utf-8"))
    video_type = redis_db.hget(event.user_id, "video_type").decode("utf-8")
    db_user_id = get_user_db_id(event.user_id)
    body = None
    if redis_db.hexists(event.user_id, "content"):
        body = {
            "content": redis_db.hget(event.user_id, "content").decode("utf-8"),
        }
        redis_db.hdel(event.user_id, "content")
    api_status = post_solution_to_api(video_id, db_user_id, type=video_type, body=body)
    logger.info(
        f"Solution commit from <{db_user_id}: {video_id} {video_type}> status: {api_status}"
    )
    return api_status
