from aiogram import types, Dispatcher


async def start(message : types.message):
    text = 'Привет, отправь мне ссылку на видео c Tiktok, и я скачаю его для тебя ^_^'
    await message.answer(text)

def handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])    