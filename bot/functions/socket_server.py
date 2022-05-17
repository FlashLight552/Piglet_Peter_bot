import asyncio

from config.config import SOCKET_SERVER_IP, SOCKET_SERVER_PORT
from config.create_bot import telegram_bot as bot
from functions.sql import Database


async def handle_echo(reader, writer):
    data = await reader.read(1024)
    message = data.decode()
    split_msg = message.split('&&&')

    user_id, date, text = split_msg

    db = Database()
    db.remind_app_save(user_id, text, date)
    
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