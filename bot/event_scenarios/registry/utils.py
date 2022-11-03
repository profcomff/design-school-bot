from bot.schemas.models import Year
from bot.event_scenarios.msg_reactions import Registry


class Name:
    def __init__(self, fio: str):
        self.success = False
        self.fio = fio.split()
        if len(self.fio) == 3:
            self.name = self.fio[1].capitalize()
            self.last_name = self.fio[0].capitalize()
            self.middle_name = self.fio[3].capitalize()
            self.success = True

    def is_valid(self):
        return self.success
