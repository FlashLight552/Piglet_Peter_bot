from aiogram.utils import executor
import logging

from create_bot import dp
from handler import tk, start, speech_recognition

# Логи
logging.basicConfig(level=logging.INFO)

# Коннект хендлеров
start.handlers_start(dp)
tk.handlers_tiktok(dp)
speech_recognition.handlers_sr(dp)

# Старт 
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
