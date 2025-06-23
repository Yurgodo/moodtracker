import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import database as db
import handlers
from scheduler import create_scheduler
from keyboards import main_kb

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def main() -> None:
    await db.init_db()

    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    bot.owner_id = (await bot.get_me()).id

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.router)

    scheduler = create_scheduler(bot)
    scheduler.start()

    @dp.message(commands=['start'])
    async def cmd_start(message: types.Message):
        await message.answer('Привет! Я бот для трекинга эмоций.', reply_markup=main_kb)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

