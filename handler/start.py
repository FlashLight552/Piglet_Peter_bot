from aiogram import types, Dispatcher
from data.btn import help_inline

async def start(message : types.message):
    text = 'Привет ^_^'
    await message.answer(text, reply_markup=help_inline)

async def help_btn(call: types.CallbackQuery):
    text = 'Итак, что я умею? \n\nЯ могу скачать видео с Tiktok, просто отправь мне ссылку. \n\nА еще могу переводить голосовые сообщения в текст, достаточно лишь переслать мне его или самому записать. '\
            '\n\nНу и последнее, но не по значению, я умею переводить текст на разные языки. Напиши мне "Перевод" и я переведу слова или целый текст.'
    await call.message.answer(text)

def handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])    
    dp.register_callback_query_handler(help_btn, text='help')