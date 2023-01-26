import sqlite3
from datetime import datetime, timedelta


def check_date(str_date):
    datetime_object = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
    return datetime.now().replace(microsecond=0) == datetime_object


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()


    # users
    # users
    # users


    def user_exists(self, user_tg_id):
        """Проверяем, есть ли юзер в базе"""
        self.cursor.execute("UPDATE `SQLITE_SEQUENCE` SET `seq` = 0")
        self.conn.commit()
        result = self.cursor.execute(
            "SELECT `id` FROM `users` WHERE `user_tg_id` = ?", (user_tg_id,))
        return bool(len(result.fetchall()))


    def get_user_id(self, user_tg_id):
        """Достаем id юзера в базе по его user_tg_id"""
        result = self.cursor.execute(
            "SELECT `id` FROM `users` WHERE `user_tg_id` = ?", (user_tg_id,))
        return result.fetchone()[0]


    def get_username(self, id_):
        """Достаем usernames юзера в базе"""
        result = self.cursor.execute("SELECT `username` FROM `users` WHERE `id` = ?", (id_,))
        return result.fetchone()[0]


    def get_tg_id(self, id_):
        result = self.cursor.execute("SELECT `user_tg_id` FROM `users` WHERE `id` = ?", (id_,))
        return result.fetchone()[0]


    def add_user(self, user_tg_id, first_name, username):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_tg_id`, `first_name`, `username`) VALUES (?, ?, ?)",
                            (user_tg_id, first_name, username))
        return self.conn.commit()


    def check_role(self, user_tg_id):
        if self.user_exists(user_tg_id):
            result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_tg_id` = ? AND `role` IS NOT NULL", (user_tg_id,))
            return bool(len(result.fetchall()))

        return False


    def edit_role(self, user_tg_id, role):
        self.cursor.execute("UPDATE `users` SET `role` = ? WHERE `user_tg_id` = ?", (role, user_tg_id))
        return self.conn.commit()


    # houses9
    # houses9
    # houses9

    def get_all_houses9(self):
        result = self.cursor.execute("SELECT * FROM `houses9`")
        return result.fetchall()


    def get_house9(self, id):
        result = self.cursor.execute("SELECT * FROM `houses9` WHERE `id` = ?", (id,))
        return result.fetchone()


    def sub_add_house9(self, n, house9_id):
        for i in range(1, n+1):
            self.add_house9_floor(i, house9_id)
        return


    def add_house9(self, address, head, comment, phone):
        self.cursor.execute("INSERT INTO `houses9` (`address`, `head`, `comment`, `phone`) VALUES (?, ?, ?, ?)",
                            (address, head, comment, phone))
        self.conn.commit()
        house9_id = self.cursor.execute("SELECT `id` FROM `houses9` WHERE `address` = ?", (address,)).fetchone()[0]

        self.sub_add_house9(9, house9_id)
        return house9_id


    def edit_data_house9(self, id, field, data):
        self.cursor.execute(f"UPDATE `houses9` SET `{field}` = ? WHERE `id` = ?", (data, id))
        return self.conn.commit()


    # floors house9
    # floors house9
    # floors house9


    def get_house9_floors(self, house9_id):
        result = self.cursor.execute("SELECT `id` FROM `floors9` WHERE `house9_id` = ?", (house9_id,))
        return [k[0] for k in result.fetchall()]


    def get_floor9(self, id):
        result = self.cursor.execute("SELECT * FROM `floors9` WHERE `id` = ?", (id,))
        return result.fetchone()


    def sub_add_floor9(self, floor9_id):
        self.add_house9_sector("Left", floor9_id)
        self.add_house9_sector("Right", floor9_id)
        return


    def add_house9_floor(self, number, house9_id):
        self.cursor.execute("INSERT INTO `floors9` (`number`, `house9_id`) VALUES (?, ?)",
                            (number, int(house9_id)))

        floor9_id = self.cursor.execute("SELECT `id` FROM `floors9` WHERE `number` = ? AND `house9_id` = ?", 
                                        (number, int(house9_id)))

        self.sub_add_floor9(floor9_id.fetchone()[0])

        return self.conn.commit()


    def edit_comment_floor9(self, id, comment):
        print(id)
        self.cursor.execute("UPDATE `floors9` SET `comment` = ? WHERE `id` = ?", (comment, id))
        return self.conn.commit()


    # sectors house9
    # sectors house9
    # sectors house9


    def sub_add_house9_sector(self, sector9_id, name, floor):
        if name == "Left":
            for i in range(1, 18):
                self.add_room9_blank(int(f"{floor}{'0' if i // 10 < 1 else ''}{i}"), sector9_id)
        elif name == "Right":
            for i in range(18, 35):
                self.add_room9_blank(int(f"{floor}{i}"), sector9_id)
        return


    def add_house9_sector(self, name, floor9_id):
        self.cursor.execute("INSERT INTO `sectors9` (`name`, `floor9_id`) VALUES (?, ?)",
                            (name, int(floor9_id)))

        sector9 = self.cursor.execute("SELECT `id`, `name` FROM `sectors9` WHERE `name` = ? AND `floor9_id` = ?", (name, floor9_id)).fetchone()
        self.sub_add_house9_sector(sector9[0], sector9[1], self.get_floor9(floor9_id)[1])
        return self.conn.commit()


    def get_sectors9(self, floor9_id):
        result = self.cursor.execute("SELECT `name`, `id` FROM `sectors9` WHERE `floor9_id` = ?", (floor9_id,))
        return {k[0]:k[1] for k in result.fetchall()}


    def get_sector9(self, id):
        result = self.cursor.execute("SELECT * FROM `sectors9` WHERE `id` = ?", (id,))
        return result.fetchone()


    def edit_sector9_comment(self, id, comment):
        self.cursor.execute("UPDATE `sectors9` SET `comment` = ? WHERE `id` = ?", (comment, id))
        return self.conn.commit()


    # rooms9
    # rooms9
    # rooms9


    def get_rooms9(self, sector9_id):
        result = self.cursor.execute("SELECT `number`, `id` FROM `rooms9` WHERE `sector9_id` = ?", (sector9_id,))
        return {k[0]:k[1] for k in result.fetchall()}


    def get_room9(self, id):
        result = self.cursor.execute("SELECT * FROM `rooms9` WHERE `id` = ?", (id,))
        return result.fetchone()


    def add_room9_blank(self, number, sector9_id):
        self.cursor.execute("INSERT INTO `rooms9` (`number`, `sector9_id`) VALUES (?, ?)", 
            (number, sector9_id))
        return self.conn.commit()


    def add_room9(self, number, sector9_id, comment, phone, status):
        self.cursor.execute("INSERT INTO `rooms9` (`number`, `sector9_id`, `comment`, `phone`, `status`) VALUES (?, ?, ?, ?, ?)", 
            (number, sector9_id, comment, phone, status))
        self.conn.commit()

        result = self.cursor.execute("SELECT `id` FROM `rooms9` WHERE `number` = ? AND `sector9_id` = ? AND `comment` = ? AND `phone` = ? AND `status` = ?", 
            (number, sector9_id, comment, phone, status))
        return result.fetchone()[0]


    def edit_data_room9(self, id, field, data):
        self.cursor.execute(f"UPDATE `rooms9` SET `{field}` = ? WHERE `id` = ?", (data, id))
        return self.conn.commit()


    # reminders
    # reminders
    # reminders


    def create_reminder(self, comment, time, user, room9_id=None, calltable_id=None):
        self.cursor.execute("INSERT INTO `reminders` (`room9_id`, `comment`, `time`, `user`, `calltable_id`) VALUES (?, ?, ?, ?, ?)", 
            (room9_id, comment, time, user, calltable_id))
        return self.conn.commit()


    def get_todays_reminders(self):
        self.conn.create_function("CHECKDATE", 1, check_date)
        result = self.cursor.execute("SELECT * FROM `reminders` WHERE CHECKDATE(`time`) = 1")
        return result.fetchall()


    def update_reminder(self, id, time):
        self.cursor.execute("UPDATE `reminders` SET `time` = ? WHERE `id` = ?", (time, id))
        return self.conn.commit()


    def delete_reminder(self, id):
        self.cursor.execute("DELETE FROM `reminders` WHERE `id` = ?", (id,))
        return self.conn.commit()


    def get_reminder(self, id):
        result = self.cursor.execute("SELECT * FROM `reminders` WHERE `id` = ?", (id,))
        return result.fetchone()


    # reserve
    # reserve
    # reserve


    def add_reserve(self, url, comment):
        self.cursor.execute("INSERT INTO `calltable` (`url`, `comment`) VALUES (?, ?)", 
            (url, comment))
        self.conn.commit()
        result = self.cursor.execute("SELECT `id` FROM `calltable` WHERE `url` = ?", (url,))
        return result.fetchone()[0]


    def delete_reserve(self, id):
        self.cursor.execute("DELETE FROM `calltable` WHERE `id` = ?", (id,))
        return self.conn.commit()


    def get_reserves(self):
        result = self.cursor.execute("SELECT * FROM `calltable`")
        return result.fetchall()


    def get_reserve(self, id):
        result = self.cursor.execute("SELECT * FROM `calltable` WHERE `id` = ?", (id,))
        return result.fetchone()


    # close

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
