from aiogram import executor
from dispatcher import dp
import handlers
# from run_reminders import start
import run_reminders
import asyncio

from db import BotDB
BotDB = BotDB('base.db')

if __name__ == "__main__":
    asyncio.ensure_future(run_reminders.start(BotDB))
    executor.start_polling(dp, skip_updates=True)
