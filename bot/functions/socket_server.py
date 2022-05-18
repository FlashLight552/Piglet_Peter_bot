import asyncio

from config.config import SOCKET_SERVER_IP, SOCKET_SERVER_PORT
from config.create_bot import telegram_bot as bot
from functions.sql import Database

import datetime
from datetime import datetime as dt
import pytz


async def handle_echo(reader, writer):
    data = await reader.read(1024)
    message = data.decode()
    split_msg = message.split('&&&')

    user_id, date, text = split_msg
    db = Database()
    timezone_db = db.user_data_request(user_id, 'tz')

    tz_time = dt.now(pytz.timezone(timezone_db)).replace(second=0, microsecond=0)
    date_strp = dt.strptime(date, '%Y-%m-%d %H:%M')

    tz = (str(tz_time)[19:])
    hours = tz[1:3]
    if tz[0] == '+':
        utc_time = date_strp - datetime.timedelta(hours=int(hours))
    utc_time = date_strp + datetime.timedelta(hours=int(hours))

    async def save(user_id, text, utc_time):
        db = Database()
        db.remind_app_save(user_id, text, utc_time)
    
    save(user_id, text, utc_time)
    
    await bot.send_message(user_id, f'Создал напоминание.\n\nНапомнить: {text}\nДата: {date}')
    writer.close()

async def server_start():
    server = await asyncio.start_server(
        handle_echo, SOCKET_SERVER_IP, SOCKET_SERVER_PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Start socket server on {addrs}')

    async with server:
        await server.serve_forever()


# asyncio.run(server_start())