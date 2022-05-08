from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from data.btn import *
from create_bot import telegram_bot


async def start(message: types.message):
    text = 'Привет ^_^'
    await message.answer(text, reply_markup=help_inline, disable_notification=True)

async def start_language(message: types.message):
    text = 'Выбери язык'
    await message.answer(text, reply_markup=lang_for_inline_tts, disable_notification=True)

async def help_btn(call: types.CallbackQuery):
    me = await telegram_bot.get_me()
    text = 'Итак, что я умею?'\
        '\n\nЯ умею качать видео с Tiktok или посты с Instagram по отправленной ссылке.'\
        '\n\nМогу переводить голосовые сообщения в текст, переводить их на другие языки и озвучивать.'\
        '\n\nПомогу перевести слова на другие языки, достаточно написать мне то, что нужно перевести.'\
        '\n\nУмею распозновать музыку, отправь мне голосовое сообщение с играющей музыкой.'  \
        f'\n\nЕще работаю в инлайн режиме. Позови меня @{me.username} и напиши что-то и я это озвучу. '\
            'Так-же можно прислать ссылку на Tiktok видео.'
    
    await call.message.answer(text, disable_notification=True)

async def language_selector(call: types.callback_query, state: FSMContext):
    async with state.proxy() as proxy:
        lang = str(call.data)
        proxy['language'] = lang.split('_')[1]
    await call.message.answer('Сохранил', disable_notification=True)


def handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_language, CommandStart('language'))
    dp.register_message_handler(start, CommandStart())

    dp.register_callback_query_handler(help_btn, text='help')

    dp.register_callback_query_handler(language_selector, text='inl_uk')
    dp.register_callback_query_handler(language_selector, text='inl_ru')
    dp.register_callback_query_handler(language_selector, text='inl_en')
    dp.register_callback_query_handler(language_selector, text='inl_de')
    dp.register_callback_query_handler(language_selector, text='inl_es')
    dp.register_callback_query_handler(language_selector, text='inl_pl')