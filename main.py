from aiogram.utils import executor
import logging

from create_bot import dp
from handler import instagram, tiktok, start, speech_recognition, translate, tts_google, inline_mod, shazam


# Логи
logging.basicConfig(level=logging.INFO)

# Коннект хендлеров
start.handlers_start(dp)
tiktok.handlers_tiktok(dp)
speech_recognition.handlers_sr(dp)
translate.handlers_translate(dp)
tts_google.handlers_tts_google(dp)  
instagram.intdl_hendler(dp)
inline_mod.handlers_inline_mod(dp)
shazam.handlers_shazam(dp)

# Старт -
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
