from aiogram import Bot, Dispatcher
from data.config import token


telegram_bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher()








# telegram_bot = Bot(token=token, parse_mode="HTML")
# dp = Dispatcher()





# dp = Dispatcher(telegram_bot, storage=storage)

    