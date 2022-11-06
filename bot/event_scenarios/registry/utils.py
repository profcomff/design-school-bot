from bot.schemas.models import Year
from bot.event_scenarios.msg_reactions import Registry


class Name:
    def __init__(self, fio: str):
        self.success = False
        self.fio = fio.split()
        if len(self.fio) == 2:
            self.name = self.fio[1].capitalize()
            self.last_name = self.fio[0].capitalize()
            self.success = True

    def is_valid(self):
        return self.success


class Direction:
    def __init__(self, db_id: int, name: str, ref: str):
        self.db_id = db_id
        self.name = name
        self.ref = ref


def get_directions() -> list[Direction]:
    return [
        Direction(1, "Фото: графия", "https://vk.com/@she_em-fotografiya"),
        Direction(2, "Контент: менеджмент", "https://vk.com/@she_em-kontent"),
        Direction(3, "Дизайн: айдентика", "https://vk.com/@she_em-aidentika"),
        Direction(4, "Дизайн: соцсети", "https://vk.com/@she_em-dizain-socseti"),
    ]
