from aiogram import types
from aiogram.types import InputFile
from dispatcher import *
from bot import BotDB
import keyboards as kb
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import ADMIN
import commands as cmds
from typing import Union
from config import SUPER_GROUP
from datetime import datetime
from dateutil.relativedelta import relativedelta


s = {"Left": "Первый", "Right": "Второй"}


# start ----------------------------------------
# start ----------------------------------------
# start ----------------------------------------


@dp.message_handler(commands="add")
async def add_wl(message: types.Message):
    user = message.from_user.id
    if int(user) == int(ADMIN):
        _, user_2 = message.text.split(" ")
        BotDB.edit_role(user_2, 0)
        await bot.send_message(user, f"{user_2} Добавлен в белый список")


@dp.message_handler(commands="remove")
async def add_wl(message: types.Message):
    user = message.from_user.id
    if int(user) == int(ADMIN):
        _, user_2 = message.text.split(" ")
        BotDB.edit_role(user_2, None)
        await bot.send_message(user, f"{user_2} Удален из белого списка")


@dp.message_handler(commands="start")
async def start(message: types.Message):
    user = message.from_user.id

    if not BotDB.user_exists(user):
        BotDB.add_user(user, message.from_user.first_name, message.from_user.username)

    if BotDB.check_role(user):
        await bot.send_message(user, 
                               f"Выберете команду:",
                               reply_markup=kb.main_kb())


@dp.message_handler(lambda msg: not BotDB.check_role(msg.from_user.id))
async def check_role(message: types.Message):
    return
@dp.callback_query_handler(lambda c: not BotDB.check_role(c.from_user.id))
async def c_banned(callback_query: types.CallbackQuery):
    return


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('main'))
async def pc_add_house9(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id

    await callback_query.message.edit_text(f"text",
                                           reply_markup=kb.main_kb())


# house9 --------------------------------------------------------------------------------------------------- 
# house9 ---------------------------------------------------------------------------------------------------
# house9 ---------------------------------------------------------------------------------------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('houses9'))
async def pc_add_house9(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    houses9 = BotDB.get_all_houses9()
    
    msg = "Девятиэтажки:\n\n"
    for i in houses9:
        msg += f"🏢<b>Общежитие №{i[0]}</b>\n<b>Адрес:</b> <i>{i[1]}</i>\n\n👨‍💼<b>Заведующий:</b> <i>{i[2]}</i>\n📱<b>Контакт:</b> <code>{i[4]}</code>\n❕<b>Комментарий:</b> <i>{i[3]}</i>\n\n"

    await callback_query.message.edit_text(msg,
                                           reply_markup=kb.houses9_inkb(tuple(k[0] for k in houses9)))


# edit house9 ----------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_house9'))
async def pc_edit_houses9(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    callback_dict = cmds.define_callback_data(callback_query.data)
    house9 = BotDB.get_house9(callback_dict.get("edit_house9"))

    await callback_query.message.edit_text(f"Какие данные вы хотите изменить в общежитии <b>№{callback_dict.get('edit_house9')}</b>?\n\n"
                                           f"🏢<b>Общежитие №{house9[0]}</b>\n<b>Адрес:</b> <i>{house9[1]}</i>\n\n👨‍💼<b>Заведующий:</b> <i>{house9[2]}</i>\n📱<b>Контакт:</b> <code>{house9[4]}</code>\n❕<b>Комментарий:</b> <i>{house9[3]}</i>",
                                           reply_markup=kb.edit_house9(callback_dict.get("edit_house9")))


class EditHouse9StatesGroup(StatesGroup):
    house9_id = State()
    field = State()
    data = State()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('change_house9'))
async def pc_edit_houses9_select(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    callback_dict = cmds.define_callback_data(callback_query.data)
    await callback_query.message.edit_text("Введите данные:")
    await EditHouse9StatesGroup.data.set()
    await state.update_data(house9_id=callback_dict.get("change_house9"))
    await state.update_data(field=callback_dict.get("thing"))


@dp.message_handler(state=EditHouse9StatesGroup.data)
async def p_edit_houses9_data(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        pass

    BotDB.edit_data_house9(data["house9_id"], data["field"], message.text)
    await state.finish()

    house9 = BotDB.get_house9(data["house9_id"])
    floors = BotDB.get_house9_floors(house9[0])

    await bot.send_message(user,
                           f"🏢<b>Общежитие №{house9[0]}</b>\n"
                           f"<b>Адрес:</b> <i>{house9[1]}</i>\n\n"
                           f"👨‍💼<b>Заведующий:</b> <i>{house9[2]}</i>\n"
                           f"📱<b>Контакт:</b> <code>{house9[4]}</code>\n"
                           f"❕<b>Комментарий:</b> <i>{house9[3]}</i>",
                           reply_markup=kb.houses9_floors_inkb(floors, house9[0]))


# add house9 ----------------------


class House9StatesGroup(StatesGroup):
    address = State()
    head = State()
    phone = State()
    comment = State()



@dp.callback_query_handler(lambda c: c.data and c.data.startswith('add_house9'))
async def pc_add_house9(callback_query: types.CallbackQuery):
    user = callback_query.message.from_user.id

    await callback_query.message.edit_text("Введите адрес девятиэтажки:",
                                           reply_markup=kb.back_inkb("blank"))
    await House9StatesGroup.address.set()


@dp.message_handler(state=House9StatesGroup.address)
async def add_house9_address(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        data['address'] = message.text

    await bot.send_message(user,
                           "Укажите заведующего девятиэтажкой \nИли нажмите кнопку \"нет\":",
                           reply_markup=kb.back_inkb("pc_add_house9"))
    await House9StatesGroup.next()


@dp.message_handler(state=House9StatesGroup.head)
async def add_house9_head(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        data['head'] = message.text

    await bot.send_message(user,
                           "Укажите номер для контакта:",
                           reply_markup=kb.back_inkb("pc_add_house9"))
    await House9StatesGroup.next()


@dp.message_handler(state=House9StatesGroup.phone)
async def add_house9_phone(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        data['phone'] = message.text

    await bot.send_message(user,
                           "Напишите комментарий для этого общежития:",
                           reply_markup=kb.back_inkb("pc_add_house9"))
    await House9StatesGroup.next()


@dp.message_handler(state=House9StatesGroup.comment)
async def add_house9_comment(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        data['comment'] = message.text

    house9_id = BotDB.add_house9(data["address"], data["head"], data["comment"], data["phone"])
    house9 = BotDB.get_house9(house9_id)

    floors = BotDB.get_house9_floors(house9_id)

    await bot.send_message(user,
                           f"🏢<b>Общежитие №{house9[0]}</b>\n"
                           f"<b>Адрес:</b> <i>{house9[1]}</i>\n\n"
                           f"👨‍💼<b>Заведующий:</b> <i>{house9[2]}</i>\n"
                           f"📱<b>Контакт:</b> <code>{house9[4]}</code>\n"
                           f"❕<b>Комментарий:</b> <i>{house9[3]}</i>",
                           reply_markup=kb.houses9_floors_inkb(floors, house9_id))
    await state.finish()
    # await p_houses9(message)


# house9 select -----------------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('house9'))
async def pc_select_house9(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    callback_dict = cmds.define_callback_data(callback_query.data)

    house9 = BotDB.get_house9(callback_dict.get("house9"))
    floors = BotDB.get_house9_floors(house9[0])

    await callback_query.message.edit_text(f"🏢<b>Общежитие №{house9[0]}</b>\n"
                                           f"<b>Адрес:</b> <i>{house9[1]}</i>\n\n"
                                           f"👨‍💼<b>Заведующий:</b> <i>{house9[2]}</i>\n"
                                           f"📱<b>Контакт:</b> <code>{house9[4]}</code>\n"
                                           f"❕<b>Комментарий:</b> <i>{house9[3]}</i>",
                                           reply_markup=kb.houses9_floors_inkb(floors, house9[0]))


# house9 floors --------------------------------------------------------------------------------------------------- 
# house9 floors ---------------------------------------------------------------------------------------------------
# house9 floors ---------------------------------------------------------------------------------------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('floor9'))
async def pc_select_floor9(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    callback_dict = cmds.define_callback_data(callback_query.data)

    floor9 = BotDB.get_floor9(callback_dict.get("floor9"))
    sectors9 = BotDB.get_sectors9(floor9[0])

    await callback_query.message.edit_text(f"🏢<b>Общежитие №{floor9[2]}</b>\n"
                                           f"🛗<b>Этаж #{floor9[1]}</b>\n"
                                           f"❕<b>Комментарий:</b> <i>{floor9[3] if floor9[3] is not None else 'Нет'}</i>",
                                           reply_markup=kb.houses9_sector_inkb(sectors9, floor9[2], floor9[0]))


class EditFloor9StatesGroup(StatesGroup):
    floor9_id = State()
    data = State()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_floor9'))
async def pc_edit_floor9(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    callback_dict = cmds.define_callback_data(callback_query.data)
    await callback_query.message.edit_text("Введите комментарий:")
    await EditFloor9StatesGroup.data.set()
    await state.update_data(floor9_id=callback_dict.get("edit_floor9"))


@dp.message_handler(state=EditFloor9StatesGroup.data)
async def p_edit_floor9_data(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        pass
    BotDB.edit_comment_floor9(data["floor9_id"], message.text)
    await state.finish()

    floor9 = BotDB.get_floor9(data["floor9_id"])
    sectors9 = BotDB.get_sectors9(floor9[0])

    await bot.send_message(user,
                           f"🏢<b>Общежитие №{floor9[2]}</b>\n"
                           f"🛗<b>Этаж #{floor9[1]}</b>\n"
                           f"❕<b>Комментарий:</b> <i>{floor9[3] if floor9[3] is not None else 'Нет'}</i>",
                           reply_markup=kb.houses9_sector_inkb(sectors9, floor9[2], floor9[0]))


# house9 sectors --------------------------------------------------------------------------------------------------- 
# house9 sectors ---------------------------------------------------------------------------------------------------
# house9 sectors ---------------------------------------------------------------------------------------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('sector9'))
async def pc_select_floor9(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    callback_dict = cmds.define_callback_data(callback_query.data)

    sector9 = BotDB.get_sector9(callback_dict.get("sector9"))
    floor9 = BotDB.get_floor9(sector9[2])
    rooms9 = BotDB.get_rooms9(sector9[0])

    await callback_query.message.edit_text(f"🏢<b>Общежитие №{floor9[2]}</b>\n"
                                           f"🛗<b>Этаж #{floor9[1]}</b>\n"
                                           f"🔛<b>{s.get(sector9[1])} Сектор</b>\n"
                                           f"❕<b>Комментарий:</b> <i>{sector9[3] if sector9[3] is not None else 'Нет'}</i>",
                                           reply_markup=kb.houses9_room_inkb(sector9[0], rooms9, floor9[0]))


# edit sector9 ---------------


class EditSector9StatesGroup(StatesGroup):
    sector9_id = State()
    data = State()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_sector9'))
async def pc_edit_sector9(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    callback_dict = cmds.define_callback_data(callback_query.data)
    await callback_query.message.edit_text("Введите комментарий:")
    await EditSector9StatesGroup.data.set()
    await state.update_data(sector9_id=callback_dict.get("edit_sector9"))


@dp.message_handler(state=EditSector9StatesGroup.data)
async def p_edit_sector9_data(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        pass
    BotDB.edit_sector9_comment(data["sector9_id"], message.text)
    await state.finish()

    sector9 = BotDB.get_sector9(data["sector9_id"])
    floor9 = BotDB.get_floor9(sector9[2])
    rooms9 = BotDB.get_rooms9(sector9[0])

    await bot.send_message(user,
                           f"🏢<b>Общежитие №{floor9[2]}</b>\n"
                           f"🛗<b>Этаж #{floor9[1]}</b>\n"
                           f"🔛<b>{s.get(sector9[1])} Сектор</b>\n"
                           f"❕<b>Комментарий:</b> <i>{sector9[3] if sector9[3] is not None else 'Нет'}</i>",
                           reply_markup=kb.houses9_room_inkb(sector9[0], rooms9, floor9[0]))


# add room9 -----------------


class Rooms9StatesGroup(StatesGroup):
    sector_id = State()

    number = State()
    comment = State()
    phone = State()
    status = State()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('add_room9'))
async def pc_add_room9(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id
    callback_dict = cmds.define_callback_data(callback_query.data)

    await callback_query.message.edit_text(f"Введите номер комнаты:")
    await Rooms9StatesGroup.number.set()

    await state.update_data(sector_id=f"{callback_dict.get('add_room9')}")


@dp.message_handler(state=Rooms9StatesGroup.number)
async def p_add_room9_number(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        data['number'] = message.text

    await bot.send_message(user, f"❕Добавте комментарий:")

    await Rooms9StatesGroup.next()


@dp.message_handler(state=Rooms9StatesGroup.comment)
async def p_add_room9_comment(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        data['comment'] = message.text

    await bot.send_message(user, f"📱Добавте контакт:")

    await Rooms9StatesGroup.next()


@dp.message_handler(state=Rooms9StatesGroup.phone)
async def p_add_room9_phone(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        data['phone'] = message.text

    await bot.send_message(user, f"Напишите статус:")

    await Rooms9StatesGroup.next()


@dp.message_handler(state=Rooms9StatesGroup.status)
async def p_add_room9_status(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        data['status'] = message.text

    room9_id = BotDB.add_room9(data["number"], data["sector_id"], data["comment"], data["phone"], data["status"])
    sector9 = BotDB.get_sector9(data["sector_id"])
    floor9 = BotDB.get_floor9(sector9[2])


    await bot.send_message(user, 
                           f"🏢<b>Общежитие №{floor9[2]}</b>\n"
                           f"🛗<b>Этаж #{floor9[1]}</b>\n"
                           f"🔛<b>{s.get(sector9[1])} Сектор</b>\n\n"
                           f"🟠<b>Комната #{data['number']}</b>\n"
                           f"❕<b>Комментарий:</b> <i>{data['comment']}</i>\n"
                           f"📱<b>Контакт:</b> <code>{data['phone']}</code>\n"
                           f"❔<b>Статус:</b> <i>{data['status']}</i>",
                           reply_markup=kb.room9_inkb(sector9[0], room9_id))

    await state.finish()
    # await pc_select_floor9()


# house9 rooms --------------------------------------------------------------------------------------------------- 
# house9 rooms ---------------------------------------------------------------------------------------------------
# house9 rooms ---------------------------------------------------------------------------------------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('room9'))
async def pc_select_room(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    callback_dict = cmds.define_callback_data(callback_query.data)

    room9 = BotDB.get_room9(callback_dict['room9'])
    sector9 = BotDB.get_sector9(room9[2])
    floor9 = BotDB.get_floor9(sector9[2])

    await callback_query.message.edit_text(f"🏢<b>Общежитие №{floor9[2]}</b>\n"
                                           f"🛗<b>Этаж #{floor9[1]}</b>\n"
                                           f"🔛<b>{s.get(sector9[1])} Сектор</b>\n\n"
                                           f"🟠<b>Комната #{room9[1]}</b>\n"
                                           f"❕<b>Комментарий:</b> <i>{room9[3]}</i>\n"
                                           f"📱<b>Контакт:</b> <code>{room9[4]}</code>\n"
                                           f"❔<b>Статус:</b> <i>{room9[5]}</i>",
                                           reply_markup=kb.room9_inkb(sector9[0], room9[0]))


# edit room9 ----------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_room9'))
async def pc_edit_room9(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    callback_dict = cmds.define_callback_data(callback_query.data)

    room9 = BotDB.get_room9(callback_dict.get("edit_room9"))
    sector9 = BotDB.get_sector9(room9[2])
    floor9 = BotDB.get_floor9(sector9[2])

    await callback_query.message.edit_text(f"Какие данные вы хотите изменить в комнате <b>#{callback_dict.get('edit_room9')}</b>?\n\n"
                                           f"🏢<b>Общежитие №{floor9[2]}</b>\n"
                                           f"🛗<b>Этаж #{floor9[1]}</b>\n"
                                           f"🔛<b>{s.get(sector9[1])} Сектор</b>\n\n"
                                           f"🟠<b>Комната #{room9[1]}</b>\n"
                                           f"❕<b>Комментарий:</b> <i>{room9[3]}</i>\n"
                                           f"📱<b>Контакт:</b> <code>{room9[4]}</code>\n"
                                           f"❔<b>Статус:</b> <i>{room9[5]}</i>",
                                           reply_markup=kb.edit_room9(callback_dict.get("edit_room9"), floor9[0]))


class EditRoom9StatesGroup(StatesGroup):
    room9_id = State()
    field = State()
    data = State()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('change_room9'))
async def pc_edit_room9_select(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    callback_dict = cmds.define_callback_data(callback_query.data)
    await callback_query.message.edit_text("Введите данные:")
    await EditRoom9StatesGroup.data.set()
    await state.update_data(room9_id=callback_dict.get("change_room9"))
    await state.update_data(field=callback_dict.get("thing"))


@dp.message_handler(state=EditRoom9StatesGroup.data)
async def p_edit_room9_data(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        pass

    BotDB.edit_data_room9(data["room9_id"], data["field"], message.text)
    await state.finish()

    room9 = BotDB.get_room9(data["room9_id"])
    sector9 = BotDB.get_sector9(room9[2])
    floor9 = BotDB.get_floor9(sector9[2])

    await bot.send_message(user,
                           f"🏢<b>Общежитие №{floor9[2]}</b>\n"
                           f"🛗<b>Этаж #{floor9[1]}</b>\n"
                           f"🔛<b>{s.get(sector9[1])} Сектор</b>\n\n"
                           f"🟠<b>Комната #{room9[1]}</b>\n"
                           f"❕<b>Комментарий:</b> <i>{room9[3]}</i>\n"
                           f"📱<b>Контакт:</b> <code>{room9[4]}</code>\n"
                           f"❔<b>Статус:</b> <i>{room9[5]}</i>",
                           reply_markup=kb.room9_inkb(sector9[0], room9[0]))


# reminders ----------------------------------------------
# reminders ----------------------------------------------
# reminders ----------------------------------------------


class RemindersStatesGroup(StatesGroup):
    room9_id = State()
    calltable_id = State()

    time = State()
    comment = State()



@dp.callback_query_handler(lambda c: c.data and c.data.startswith('set_reminder'))
async def pc_set_remind(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    callback_dict = cmds.define_callback_data(callback_query.data)
    await callback_query.message.edit_text("Напишите дату в формате \"DD.MM.YYYY H:MM\", или выберете один из вариантов ниже на 9 утра:",
                                           reply_markup=kb.set_reminders_inkb())
    await RemindersStatesGroup.time.set()

    if callback_dict.get("tag") == "room":
        await state.update_data(room9_id=callback_dict.get("set_reminder"))
    elif callback_dict.get("tag") == "reserve":
        await state.update_data(calltable_id=callback_dict.get("set_reminder"))


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('remind_time'), state=RemindersStatesGroup.time)
async def pc_set_remind_time(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    callback_dict = cmds.define_callback_data(callback_query.data)

    time = ""
    if callback_dict.get("remind_time") == "month":
        time = datetime.now().replace(microsecond=0) + relativedelta(months=+1)
    elif callback_dict.get("remind_time") == "week":
        time = datetime.now().replace(microsecond=0) + relativedelta(days=+7)
    async with state.proxy() as data:
        data["time"] = time

    await callback_query.message.edit_text("Добавте комментарий к этому уведомлению:")
    await RemindersStatesGroup.next()


@dp.message_handler(state=RemindersStatesGroup.time)
async def p_set_remind_comment(message: types.Message, state: FSMContext):
    user = message.from_user.id

    datetime_object = "time"
    async with state.proxy() as data:
        data["time"] = datetime_object
    try:
        datetime_object = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
        async with state.proxy() as data:
            data["time"] = datetime_object
        await bot.send_message(user, "Добавте комментарий к этому уведомлению:")
        await RemindersStatesGroup.next()
    except:
        await bot.send_message(user, "Введена некоректная дата, попробуйте еще раз")


@dp.message_handler(state=RemindersStatesGroup.comment)
async def pc_set_remind_comment(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        pass

    BotDB.create_reminder(message.text, data["time"], user, data.get("room9_id", None), data.get("calltable_id", None))
    await bot.send_message(user, "Уведомление создано")

    

    if data.get("room9_id", None) is not None:
        room9 = BotDB.get_room9(data["room9_id"])
        sector9 = BotDB.get_sector9(room9[2])
        floor9 = BotDB.get_floor9(sector9[2])

        await bot.send_message(user,
                               f"🏢<b>Общежитие №{floor9[2]}</b>\n"
                               f"🛗<b>Этаж #{floor9[1]}</b>\n"
                               f"🔛<b>{s.get(sector9[1])} Сектор</b>\n\n"
                               f"🟠<b>Комната #{room9[1]}</b>\n"
                               f"❕<b>Комментарий:</b> <i>{room9[3]}</i>\n"
                               f"📱<b>Контакт:</b> <code>{room9[4]}</code>\n"
                               f"❔<b>Статус:</b> <i>{room9[5]}</i>",
                               reply_markup=kb.room9_inkb(sector9[0], room9[0]))
    else:
        reserve = BotDB.get_reserve(data["calltable_id"])
        await bot.send_message(user,
                               f"Объявление #{reserve[0]} \n<b>url:</b> {reserve[1]} \n<b>Комментарий:</b> <i>{reserve[2]}</i>\n\n",
                               reply_markup=kb.reserve_select_inkb(reserve[0]))
    await state.finish()


# edit reminders ---------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_remind_time'))
async def pc_edit_remind_time(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id

    callback_dict = cmds.define_callback_data(callback_query.data)
    t = callback_dict.get("edit_remind_time")

    reminder = BotDB.get_reminder(callback_dict.get("reminder"))
    datetime_object = datetime.strptime(reminder[3], '%Y-%m-%d %H:%M:%S')

    if t == "delete":
        BotDB.delete_reminder(reminder[0])
        await callback_query.message.edit_text(f"Уведомление #{reminder[0]} удалено")
        return
    elif t == "day":
        BotDB.update_reminder(reminder[0], (datetime_object) + relativedelta(days=+1))
        await callback_query.message.edit_text(f"Уведомление #{reminder[0]} перенесено на день")
        return
    elif t == "week":
        BotDB.update_reminder(reminder[0], (datetime_object) + relativedelta(days=+7))
        await callback_query.message.edit_text(f"Уведомление #{reminder[0]} перенесено на неделю")
        return
    elif t == "month":
        BotDB.update_reminder(reminder[0], (datetime_object) + relativedelta(months=+1))
        await callback_query.message.edit_text(f"Уведомление #{reminder[0]} перенесено на месяц")
        return


# Reserve ----------------------------------------
# Reserve ----------------------------------------
# Reserve ----------------------------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('reserve'))
async def pc_all_reserve(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id

    reserves = BotDB.get_reserves()

    msg = "Объявления резерва\n\n"
    for i in reserves:
        msg += f"Объявление #{i[0]} \n<b>url:</b> {i[1]} \n<b>Комментарий:</b> <i>{i[2]}</i>\n\n"

    await callback_query.message.edit_text(msg, reply_markup=kb.reserve_inkb([k[0] for k in reserves]))


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('select_reserve'))
async def pc_reserve(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    callback_dict = cmds.define_callback_data(callback_query.data)

    reserve = BotDB.get_reserve(callback_dict.get("select_reserve"))

    await callback_query.message.edit_text(f"Объявление #{reserve[0]} \n<b>url:</b> {reserve[1]} \n<b>Комментарий:</b> <i>{reserve[2]}</i>\n\n", 
                                           reply_markup=kb.reserve_select_inkb(reserve[0]))


# delete reserve ----------------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('delete_reserve'))
async def pc_delete_reserve(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    callback_dict = cmds.define_callback_data(callback_query.data)

    BotDB.delete_reserve(callback_dict.get("delete_reserve"))
    reserves = BotDB.get_reserves()

    msg = "Объявления резерва\n\n"
    for i in reserves:
        msg += f"Объявление #{i[0]} \n<b>url:</b> {i[1]} \n<b>Комментарий:</b> <i>{i[2]}</i>\n\n"

    await callback_query.message.edit_text(msg, reply_markup=kb.reserve_inkb([k[0] for k in reserves]))


# add reserve ----------------------------


class ReservesStatesGroup(StatesGroup):
    url = State()
    comment = State()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('add_reserve'))
async def pc_add_reserve(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id

    await callback_query.message.edit_text("Вставьте URL:")
    await ReservesStatesGroup.url.set()


@dp.message_handler(state=ReservesStatesGroup.url)
async def p_add_reserve_url(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        data["url"] = message.text

    await bot.send_message(user, "Добавте комментарий к этому объявлению:")
    await ReservesStatesGroup.next()


@dp.message_handler(state=ReservesStatesGroup.comment)
async def p_add_reserve_comment(message: types.Message, state: FSMContext):
    user = message.from_user.id

    async with state.proxy() as data:
        pass

    reserve_id = BotDB.add_reserve(data["url"], message.text)
    reserve = BotDB.get_reserve(reserve_id)

    await bot.send_message(user,
                           f"Объявление #{reserve[0]} \n<b>url:</b> {reserve[1]} \n<b>Комментарий:</b> <i>{reserve[2]}</i>\n\n",
                           reply_markup=kb.reserve_select_inkb(reserve_id))
    await state.finish()


# Back ----------------------------------------
# Back ----------------------------------------
# Back ----------------------------------------


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('back'), state='*')
async def p_c_back(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id

    callback_dict = cmds.define_callback_data(callback_query.data)
    function_name = callback_dict.get("back")

    current_state = await state.get_state()

    if current_state is not None:
        if function_name == "blank":
            await state.finish()
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            return
        await globals()[current_state.split(":")[0]].previous()
    else:
        return

    # callback_query.message.from_user.id = user

    await globals()[function_name](callback_query)
