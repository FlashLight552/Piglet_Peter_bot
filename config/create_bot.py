from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from pathlib import Path
import asyncio

from config.config import TELEGRAM_TOKEN
from functions.sql import Database

telegram_bot = Bot(token=TELEGRAM_TOKEN)
storage = JSONStorage(Path.cwd() / "config/db/fsm_data.json")
dp = Dispatcher(telegram_bot, storage=storage)
    
async def on_startup(dp):
     asyncio.sleep(10)
     db = Database()
     db.discord_token_create_table()
     print('[+] Tables was created')

async def on_shutdown(dp):
     await dp.storage.close()
     await dp.storage.wait_closed()
     print('[+] FMS storage was saved')