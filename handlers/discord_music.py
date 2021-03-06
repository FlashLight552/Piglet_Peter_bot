from aiogram import types, Dispatcher
import aiogram.utils.markdown as fmt
from config.config import DISCORD_CHAT_ID
from functions.zenon import zenon
from functions.sql import Database
import asyncio


async def discord_token(message:types.Message):
    ds_token = message.text.split()[:14][1].replace('"','')
    
    db = Database()
    db.user_data_save(message.from_user.id, column='ds_token', data=ds_token)
    
    msg = await message.answer(f'Твой Discord token: \n\n{fmt.hspoiler(ds_token)} \n\nСообщение будет удалено через 10 секунд.',
                                types.ParseMode.HTML, disable_notification=True)
    await message.delete()
    await asyncio.sleep(10)
    await msg.delete()


async def discord_music_sender(message: types.Message):
    db = Database()
    token = db.user_data_request(message.from_user.id, 'ds_token')
    if token:
        command = message.text
        client = zenon.Client(token)
        client.send_message(DISCORD_CHAT_ID, f'!! {command}')
    else:
        await message.answer('Для начала добавь свой Discord token: \n/discord_token "TOKEN"', 
                                disable_notification=True)   


async def create(message: types.Message):
    db = Database()
    db.user_create_table()
    await message.answer('[+]', disable_notification=True)


async def info(message: types.Message):
    db = Database()
    token = db.user_data_request(message.from_user.id, 'ds_token')
    msg = await message.answer(f'Discord chat id: {fmt.hspoiler(DISCORD_CHAT_ID)}\nDiscord token: {fmt.hspoiler(token)}',
                                types.ParseMode.HTML, disable_notification=True)
    await asyncio.sleep(20)
    await msg.delete()


def discord_handler(dp: Dispatcher):
    dp.register_message_handler(discord_music_sender, regexp='(https:\/\/)?(www.|music.|youtu.|m.)?(youtube.com|be)', chat_type='private')
    dp.register_message_handler(discord_token, commands=['discord_token'])
    dp.register_message_handler(create, commands=['discord_create'])
    dp.register_message_handler(info, commands=['discord_info'])
