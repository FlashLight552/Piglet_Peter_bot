from aiogram.utils import executor
import logging

from create_bot import dp
from handler import instagram, tiktok, start, speech_recognition,\
             translate, tts_google, inline_mod, shazam, discord_music


# Логи
logging.basicConfig(level=logging.INFO)

# Коннект хендлеров
start.handlers_start(dp)

tiktok.handlers_tiktok(dp)
instagram.intdl_hendler(dp)
discord_music.discord_handler(dp)

speech_recognition.handlers_sr(dp)
tts_google.handlers_tts_google(dp)
shazam.handlers_shazam(dp)

inline_mod.handlers_inline_mod(dp)
translate.handlers_translate(dp)


# Старт -
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
