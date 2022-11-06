from bot.schemas.models import Directions
from dataclasses import dataclass


@dataclass
class Start:
    START_BUTTON: str = "Начать"


@dataclass
class Spam:
    START_MESSAGE = "Привет!"
    START_BUTTON = "Хочу на ШЭ ЭМ"
    START_REPLY = "Мы добавили тебя в список"


@dataclass
class Registry:
    START_MESSAGE = """Привет, мы принесли тебе новость нереальной крутости!\n
    Сядь, а то упадёшь — РЕГИСТРАЦИЯ НА ШЭ ЭМ ОТКРЫТА!\n
    Теперь всё просто — нажимай кнопку «Регистрация» и следуй инструкции."""
    START_BUTTON = "Зарегистрироваться!"
    FIO_QUESTION = "Скажи свое ФИО в формате “Фамилия Имя Отчество”"
    ON_FAILURE = "Неправильный формат, введи данные ещё раз)"
    UNION_QUESTION = "Напиши номер своего профсоюзного билета"
    YEAR_QUESTION = (
        "На каком курсе учишься? Напиши в формате “1” или “1м” (если ты магистр)"
    )
    DIRECTION_QUESTION = """Выбери направление -- можно выбрать только одно,
     а изменить его в процессе Школы будет нельзя!
     Направления: 
     Фото: графия https://vk.com/@she_em-fotografiya
     Контент: менеджмент https://vk.com/@she_em-kontent
     Дизайн: соцсетей https://vk.com/@she_em-aidentika
     Дизайн: айдентика https://vk.com/@she_em-dizain-socseti
     """
    APPROVE_QUESTION = "Это точно?"
    APPROVE_TRUE = "Да!"
    APPROVE_FALSE = "Нет"
    ABOUT_QUESTION = "Расскажи, что ты уже умеешь, есть ли у тебя опыт в этой области?"
    ON_CV_ANSWER = """Классно, будем знакомы! 
    Мы тебя зарегистрировали, с 15 ноября можно будет начать учиться.
    А до этого мы пришлём тебе ссылку на чат с кураторами и остальными участниками (подмигивающий смайлик)
    """
