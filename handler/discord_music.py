from cmath import pi
from aiogram import types, Dispatcher
from data.config import DISCORD_TOKEN, CHAT_ID
from function.zenon import zenon

async def discord_music_sender(message: types.Message):
    command = message.text
    client = zenon.Client(DISCORD_TOKEN)
    client.send_message(CHAT_ID, f'!! {command}')
    

def discord_handler(dp: Dispatcher):
    dp.register_message_handler(discord_music_sender, regexp='(https:\/\/)?(www.|music.|youtu.|m.)?(youtube.com|be)', chat_type='private')
