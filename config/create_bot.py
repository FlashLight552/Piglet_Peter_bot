from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from pathlib import Path

from config.config import TELEGRAM_TOKEN


telegram_bot = Bot(token=TELEGRAM_TOKEN)
storage = JSONStorage(Path.cwd() / "config/db/fsm_data.json")
dp = Dispatcher(telegram_bot, storage=storage)
    