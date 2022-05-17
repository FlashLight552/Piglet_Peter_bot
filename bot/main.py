import asyncio
from time import sleep
from aiogram.utils import executor
import logging

from config.create_bot import dp
from handlers import instagram, tiktok, start, speech_recognition,\
             translate, tts_google, inline_mod, shazam, discord_music, remind

from functions.sql import Database
from functions.socket_server import server_start
from functions.remind import remind_check

# Логи
logging.basicConfig(level=logging.INFO)

# Коннект хендлеров
start.handlers_start(dp)

tiktok.handlers_tiktok(dp)
instagram.intdl_hendler(dp)
discord_music.discord_handler(dp)

remind.handlers_remind(dp)
    
speech_recognition.handlers_sr(dp)
tts_google.handlers_tts_google(dp)
shazam.handlers_shazam(dp)

inline_mod.handlers_inline_mod(dp)
translate.handlers_translate(dp)


if __name__ == '__main__':
    db = Database()
    while True:
        try:
            db.create_tables()
        except:
            print('Try to connect again')
            sleep(2)
        else:
            break
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(server_start())
    loop.create_task(remind_check())

    executor.start_polling(dp, skip_updates=True)
