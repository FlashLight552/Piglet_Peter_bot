from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from data.btn import *


async def start(message : types.message):
    if message.text == '/start language':
        text = 'Выбери язык'
        await message.answer(text, reply_markup=lang_for_inline_tts, disable_notification=True)
    else:
        text = 'Привет ^_^'
        await message.answer(text, reply_markup=help_inline, disable_notification=True)

async def help_btn(call: types.CallbackQuery):
    text = 'Итак, что я умею? \n\nЯ могу скачать видео с Tiktok, просто отправь мне ссылку.'\
            '\n\nТакже могу по ссылке скачать пост с Instagram.'\
            '\n\nА еще могу переводить голосовые сообщения в текст, достаточно лишь переслать мне его или самому записать. '\
            '\n\nНу и последнее, но не по значению, я умею переводить текст на разные языки. Напиши мне "Перевод" и я переведу слова или целый текст.'
    await call.message.answer(text, disable_notification=True)

async def language_selector(call: types.callback_query, state: FSMContext):
    async with state.proxy() as proxy:
        lang = str(call.data)
        proxy['language'] = lang.split('_')[1]
    await call.message.answer('Сохранил', disable_notification=True)


def handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(help_btn, text='help')

    dp.register_callback_query_handler(language_selector, text='inl_uk')
    dp.register_callback_query_handler(language_selector, text='inl_ru')
    dp.register_callback_query_handler(language_selector, text='inl_en')
    dp.register_callback_query_handler(language_selector, text='inl_de')
    dp.register_callback_query_handler(language_selector, text='inl_es')
    dp.register_callback_query_handler(language_selector, text='inl_pl')