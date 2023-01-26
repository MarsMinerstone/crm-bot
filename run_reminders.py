import asyncio
# from bot import BotDB
from datetime import datetime
import config
import keyboards as kb


from aiogram import Bot
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")


s = {"Left": "Первый", "Right": "Второй"}


async def check(BotDB):
    # await bot.send_message(466411276, BotDB.get_all_houses9())
    while True:
        reminders = BotDB.get_todays_reminders()
        for i in reminders:
            if i[1] is not None:
                room9 = BotDB.get_room9(i[1])
                sector9 = BotDB.get_sector9(room9[2])
                floor9 = BotDB.get_floor9(sector9[2])

                await bot.send_message(i[4], 
                                       f"Напоминание: #{i[0]}\n\n"
                                       f"<b>Общежитие №{floor9[2]}</b>\n"
                                       f"<b>Этаж #{floor9[1]}</b>\n"
                                       f"<b>{s.get(sector9[1])} Сектор</b>\n"
                                       f"<b>Комната #{room9[1]}</b>\n"
                                       f"<b>Комментарий:</b> <i>{room9[3]}</i>\n"
                                       f"<b>Контакт:</b> <i>{room9[4]}</i>\n"
                                       f"<b>Статус:</b> <i>{room9[5]}</i>\n\n"
                                       f"<i>{i[2]}</i>",
                                       reply_markup=kb.edit_reminder_inkb(i[0])) # -> to handlers
            else:
                reserve = BotDB.get_reserve(i[5])
                await bot.send_message(i[4], 
                                       f"Напоминание: #{i[0]}\n\n"
                                       f"Объявление #{reserve[0]} \n<b>url:</b> {reserve[1]} \n<b>Комментарий:</b> <i>{reserve[2]}</i>\n\n"
                                       f"<i>{i[2]}</i>",
                                       reply_markup=kb.edit_reminder_inkb(i[0])) # -> to handlers
        await asyncio.sleep(60)


async def start(BotDB):
    current_sec = int(datetime.now().strftime("%S"))
    delay = 60 - current_sec
    if delay == 60:
        delay = 0
    #
    await asyncio.sleep(delay)
    await check(BotDB)
