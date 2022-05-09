from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from config.config import CHAT_ID
from functions.zenon import zenon
import asyncio

async def discord_token(message:types.Message, state:FSMContext):
    async with state.proxy() as proxy:
        proxy['discord_token'] = ds_token = message.text.split()[:14][1].replace('"','')
        msg = await message.answer(f'Твой Discord token: \n\n{ds_token} \n\nСообщение будет удалено через 10 секунд.')
        await message.delete()
        await asyncio.sleep(10)
        await msg.delete()
       

async def discord_music_sender(message: types.Message, state:FSMContext):
    async with state.proxy() as proxy:
        if 'discord_token' in proxy:
            token = proxy['discord_token']
            command = message.text
            client = zenon.Client(token)
            client.send_message(CHAT_ID, f'!! {command}')
        else:
            await message.answer('Для начала добавь свой Discord token: \n/discord_token "TOKEN"')   
    

def discord_handler(dp: Dispatcher):
    dp.register_message_handler(discord_music_sender, regexp='(https:\/\/)?(www.|music.|youtu.|m.)?(youtube.com|be)', chat_type='private')
    dp.register_message_handler(discord_token, commands=['discord_token'])
