from aiogram.types import \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


# main


def main_kb(admin=False):
    main_kb = InlineKeyboardMarkup()
    main_kb.add(
        InlineKeyboardButton(f'Объявления', callback_data=f'reserve'),
        InlineKeyboardButton(f'Девятиэтажки', callback_data=f'houses9'))
    if admin is True:
        main_kb.insert(InlineKeyboardButton(f'Пользователи', callback_data=f'users'))
    return main_kb


back_num2_inkb = InlineKeyboardMarkup().add(InlineKeyboardButton(f'◀️На главную', callback_data=f'main'))


def houses9_inkb(c: int, role):
    houses9_inkb = InlineKeyboardMarkup(row_width=4)
    for i in sorted(c):
        houses9_inkb.insert(InlineKeyboardButton(f'{i}', callback_data=f'house9:{i}'))
    if role == "1":
        houses9_inkb.add(
            InlineKeyboardButton(f'➕Добавить общежитие', callback_data=f'add_house9'))
    houses9_inkb.add(
        InlineKeyboardButton(f'◀️На главную', callback_data=f'main'))
    return houses9_inkb


def houses9_floors_inkb(floors, house_id, role):
    houses9_floors_inkb = InlineKeyboardMarkup(row_width=3)
    for i, floor_id in enumerate(sorted(floors)):
        houses9_floors_inkb.insert(InlineKeyboardButton(f'{i+1}', callback_data=f'floor9:{floor_id}'))
    if role == "1":
        houses9_floors_inkb.add(
            InlineKeyboardButton(f'Изменить данные', callback_data=f'edit_house9:{house_id}'))
    houses9_floors_inkb.add(
        InlineKeyboardButton(f'◀️Ко всем общежитиям', callback_data=f'houses9'))
    return houses9_floors_inkb


def edit_house9(house_id):
    """for editing data of house9"""
    edit_house9 = InlineKeyboardMarkup().add(
        InlineKeyboardButton(f'Адрес', callback_data=f'change_house9:{house_id}&thing:address')).add(
        InlineKeyboardButton(f'Заведующего', callback_data=f'change_house9:{house_id}&thing:head')).add(
        InlineKeyboardButton(f'Контакт', callback_data=f'change_house9:{house_id}&thing:phone')).add(
        InlineKeyboardButton(f'Комментарий', callback_data=f'change_house9:{house_id}&thing:comment')).add(
        InlineKeyboardButton(f'◀️Назад', callback_data=f'house9:{house_id}'))

    return edit_house9


def houses9_sector_inkb(sectors, house_id, floor_id):
    houses9_sector_inkb = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(f'Первый (1-17)', callback_data=f'sector9:{sectors.get("Left")}'),
        InlineKeyboardButton(f'Второй (18-34)', callback_data=f'sector9:{sectors.get("Right")}'),
        InlineKeyboardButton(f'Изменить комментарий', callback_data=f'edit_floor9:{floor_id}')).add(
        InlineKeyboardButton(f'◀️Ко всем этажам', callback_data=f'house9:{house_id}'),
        InlineKeyboardButton(f'◀️Ко всем общежитиям', callback_data=f'houses9'))
    return houses9_sector_inkb


def houses9_room_inkb(sector, rooms, floor_id):
    houses9_room_inkb = InlineKeyboardMarkup()
    for i in sorted(rooms):
        houses9_room_inkb.insert(InlineKeyboardButton(f'{i}', callback_data=f'room9:{rooms.get(i)}'))

    houses9_room_inkb.add(
        InlineKeyboardButton('Изменить комментарий', callback_data=f'edit_sector9:{sector}')).add(
        # InlineKeyboardButton('➕Добавить комнату', callback_data=f'add_room9:{sector}')).add(
        InlineKeyboardButton('◀️К секторам', callback_data=f'floor9:{floor_id}'),
        InlineKeyboardButton(f'◀️Ко всем общежитиям', callback_data=f'houses9'))
    return houses9_room_inkb


def room9_inkb(sector_id, room_id):
    room9_inkb = InlineKeyboardMarkup()
    room9_inkb.add(InlineKeyboardButton('Изменить данные', callback_data=f'edit_room9:{room_id}'),
        InlineKeyboardButton('⏱Поставить уведомление', callback_data=f'set_reminder:{room_id}&tag:room')).add(
        InlineKeyboardButton('◀️Ко всем комнатам', callback_data=f'sector9:{sector_id}'),
        InlineKeyboardButton(f'◀️Ко всем общежитиям', callback_data=f'houses9'))
    return room9_inkb


def edit_room9(room_id, floor_id):
    """for editing data of room9"""
    edit_room9 = InlineKeyboardMarkup().add(
        InlineKeyboardButton(f'Комментарий', callback_data=f'change_room9:{room_id}&thing:comment')).add(
        InlineKeyboardButton(f'Контакт', callback_data=f'change_room9:{room_id}&thing:phone')).add(
        InlineKeyboardButton(f'Статус', callback_data=f'change_room9:{room_id}&thing:status')).add(
        InlineKeyboardButton(f'◀️Назад', callback_data=f'floor9:{floor_id}'))

    return edit_room9


def set_reminders_inkb():
    set_reminders_inkb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(f'Через неделю', callback_data=f'remind_time:week'),
        InlineKeyboardButton(f'Через месяц', callback_data=f'remind_time:month'))
    return set_reminders_inkb


def edit_reminder_inkb(reminder_id):
    edit_reminder_inkb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(f'Удалить', callback_data=f'edit_remind_time:delete&reminder:{reminder_id}'),
        InlineKeyboardButton(f'Перенести на день', callback_data=f'edit_remind_time:day&reminder:{reminder_id}'),
        InlineKeyboardButton(f'Перенести на неделю', callback_data=f'edit_remind_time:week&reminder:{reminder_id}'),
        InlineKeyboardButton(f'Перенести на месяц', callback_data=f'edit_remind_time:month&reminder:{reminder_id}'))
    return edit_reminder_inkb


def reserve_inkb(r: int):
    reserve_inkb = InlineKeyboardMarkup(row_width=4)
    for i in sorted(r):
        reserve_inkb.insert(InlineKeyboardButton(f'{i}', callback_data=f'select_reserve:{i}'))

    reserve_inkb.add(
        InlineKeyboardButton(f'➕Добавить объявление', callback_data=f'add_reserve')).add(
        InlineKeyboardButton(f'◀️На главную', callback_data=f'main'))
    return reserve_inkb


def reserve_select_inkb(reserve_id):
    reserve_select_inkb = InlineKeyboardMarkup(row_width=4)
    reserve_select_inkb.add(
        InlineKeyboardButton(f'Изменить объявление', callback_data=f'edit_reserve:{reserve_id}'),
        InlineKeyboardButton(f'❌Удалить объявление', callback_data=f'delete_reserve:{reserve_id}'),
        InlineKeyboardButton('⏱Поставить уведомление', callback_data=f'set_reminder:{reserve_id}&tag:reserve')).add(
        InlineKeyboardButton(f'◀️Назад', callback_data=f'reserve'))
    return reserve_select_inkb


# back


def back_inkb(func_name: str):
    inline_btn_back = InlineKeyboardButton("🔙Назад", callback_data=f"back:{func_name}")
    back_inkb = InlineKeyboardMarkup().add(inline_btn_back)
    return back_inkb
