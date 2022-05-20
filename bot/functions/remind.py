import asyncio

import datetime
from datetime import datetime as dt

from functions.sql import Database
from config.create_bot import telegram_bot as bot



async def remind_check():
    while True:
        await asyncio.sleep(5)
        time_start = dt.now().replace(second=0, microsecond=0) + datetime.timedelta(minutes=1)
        time_stop = dt.now().replace(second=0, microsecond=0) + datetime.timedelta(minutes=2)
        db = Database()
        result = db.remind_app_request(time_start, time_stop)
        if result:
            remind_del_old(time_start, time_stop)
            for item in result:
                user_id, text = item
                try:
                    await bot.send_message(user_id, f'Ты просил напомнить, напоминаю.\n\n{text}\n\nХорошего дня ^_^')
                except:
                    pass
                await asyncio.sleep(0.2)


def remind_del_old(time_start, time_stop):
    db = Database()
    db.remind_app_delete(time_start, time_stop)