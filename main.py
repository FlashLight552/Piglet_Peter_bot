from aiogram.utils import executor
import logging

from create_bot import dp
from handler import insta_dl, tiktok, start, speech_recognition, translate, tts_googl


# Логи
logging.basicConfig(level=logging.INFO)

# Коннект хендлеров
start.handlers_start(dp)
tiktok.handlers_tiktok(dp)
speech_recognition.handlers_sr(dp)
translate.handlers_translate(dp)
tts_googl.handlers_tts_google(dp)
insta_dl.intdl_hendler(dp)


# Старт -
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
