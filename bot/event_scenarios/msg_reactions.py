from bot.schemas.models import Directions
from bot.event_scenarios.registry.utils import get_directions
from dataclasses import dataclass
from .registry.utils import get_directions


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
    START_MESSAGE = """Привет, мы принесли тебе новость нереальной крутости! \nСядь, а то упадёшь — РЕГИСТРАЦИЯ НА ШЭ ЭМ ОТКРЫТА! \nТеперь всё просто — нажимай кнопку «Регистрация» и следуй инструкции."""
    START_BUTTON = "Зарегистрироваться!"
    FIO_QUESTION = "Скажи свое ФИО в формате “Фамилия Имя Отчество” (отчество писать не обязательно)"
    ON_FAILURE = "Неправильный формат, введи данные ещё раз)"
    UNION_QUESTION = "Напиши номер своего профсоюзного билета"
    YEAR_QUESTION = (
        "На каком курсе учишься? Напиши в формате “1” или “1м” (если ты магистр)"
    )
    DIRECTION_QUESTION = """Выбери направление -- можно выбрать только одно, а изменить его в процессе Школы будет нельзя! 
    Направления: 
    Фото: графия https://vk.com/@she_em-fotografiya 
    Контент: менеджмент https://vk.com/@she_em-kontent 
    Дизайн: соцсети https://vk.com/@she_em-dizain-socseti
    Дизайн: айдентика https://vk.com/@she_em-aidentika 
    """
    APPROVE_QUESTION = "Это точно?"
    APPROVE_TRUE = "Да!"
    APPROVE_FALSE = "Нет"
    ABOUT_QUESTION = "Расскажи, что ты уже умеешь, есть ли у тебя опыт в этой области?"
    ON_CV_ANSWER = """Классно, будем знакомы! Мы тебя зарегистрировали, с 15 ноября можно будет начать учиться. А до этого мы пришлём тебе ссылку на чат с кураторами и остальными участниками 😉 """


@dataclass
class Workflow:
    @classmethod
    def start_message(cls, direction_id: int):
        return f"""ARE YOU READYYYY?? Мы уже держим палец над кнопкой, которая откроет тебе доступ к курсу '{get_directions()[direction_id].name}'. Тебе осталось только прочитать небольшую инструкцию и нажать кнопку «Всё понятно». После нажатия кнопки бот пришлет тебе первое видео. Когда посмотришь его, нажимай кнопку “К следующему уроку”. После некоторых уроков тебя будут ждать проверочные задания — делать их или нет, решать тебе. А иногда будут встречаться контрольные задания — они обязательные, их нужно сделать и прислать боту, чтобы открыть доступ к следующим урокам. Внимательно читай, что тебе нужно прислать боту — ссылку на гугл-диск, файл или просто текст. Если у тебя возникнут вопросы по курсу, установке или интерфейсу программ, организационным моментам или чему-то ещё, просто напиши в чат курса, и кураторы помогут тебе. Вот и всё, теперь погнали!” """

    REGISTRY_EXPIRED = """Ой, кажется уже слишком поздно. Регистрация на ШЭ ЭМ уже закончилась, и мы не можем тебя добавить. Но есть и хорошая новость — скоро здесь будет что-то супер-пупер-дупер интересное! Подпишись на уведомления группы, чтобы не пропустить."""
    CONFIRM_BUTTON = """Всё понятно"""
    NEXT_VIDEO_BUTTON = """К следующему уроку"""
