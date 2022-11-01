from bot.routes import longpoll
from logic import process_event
from logging import getLogger
import logging


logging.basicConfig(
    filename=f"logger_{__name__}.log",
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


if __name__ == "__main__":
    logger = getLogger(__name__)
    try:
        while True:
            for event in longpoll.listen():
                process_event(event)
    except Exception as e:
        logger.critical(repr(e))
