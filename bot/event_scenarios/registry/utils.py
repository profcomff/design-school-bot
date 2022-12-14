class Name:
    def __init__(self, fio: str):
        self.success = False
        self.fio = fio.split()
        self.middle_name = "-"
        if len(self.fio) == 2:
            self.name = self.fio[1].capitalize()
            self.last_name = self.fio[0].capitalize()
            self.success = True
        elif len(self.fio) == 3:
            self.name = self.fio[1].capitalize()
            self.last_name = self.fio[0].capitalize()
            self.middle_name = self.fio[2].capitalize()
            self.success = True

    def is_valid(self):
        return self.success


class Direction:
    def __init__(self, db_id: int, name: str, ref: str, chat_ref="", end_link=""):
        self.db_id = db_id
        self.name = name
        self.ref = ref
        self.chat_ref = chat_ref
        self.end_link = end_link


def get_directions() -> list[Direction]:
    return [
        Direction(
            1,
            "Фото: графия",
            "https://vk.com/@she_em-fotografiya",
            chat_ref="https://vk.me/join/qafLjvPhU7rLk/yJ5gY2y4qjxtui8cI5OTQ=",
            end_link="https://forms.gle/67yAWqBapqYh5y2e6",
        ),
        Direction(
            2,
            "Контент: менеджмент",
            "https://vk.com/@she_em-kontent",
            chat_ref="https://vk.me/join/enw/324naMhGhn5IVXA0q9ST54PQDq0mneI=",
            end_link="https://forms.gle/X6HuSWBgJNfWawJ37",
        ),
        Direction(
            3,
            "Дизайн: айдентика",
            "https://vk.com/@she_em-aidentika",
            chat_ref="https://vk.me/join/jdKuxztKMJ1C0JYiPbgbsHDE2_me_A9WbRM=",
            end_link="https://forms.gle/kNhnW8PVAx7AAELn7",
        ),
        Direction(
            4,
            "Дизайн: соцсети",
            "https://vk.com/@she_em-dizain-socseti",
            chat_ref="https://vk.me/join/Son4hsUH76DeK6Bg/ti0Dqz4UPo91Vl/Z90=",
            end_link="vk.cc/ciQ69G",
        ),
    ]
