from bot.config.vk_session import longpoll, vk
from bot.event_scenarios.layout import process_event
from logging import getLogger
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


if __name__ == "__main__":
    logger = getLogger(__name__)
    while True:
        longpoll.update_longpoll_server()
        try:
            for event in longpoll.check():
                process_event(vk, event)
        except Exception as e:
            logger.critical(repr(e))
