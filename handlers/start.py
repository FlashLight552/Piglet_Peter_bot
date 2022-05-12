from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart

from config.btn import *
from config.config import OWNER
from config.create_bot import telegram_bot
from functions.sql import Database


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
            'Так-же можно прислать ссылку на Tiktok видео.'\
        '\n\nNew!\nVoice assistant. Отправь голосовое сообщение с командой:\n'\
        '- Youtube или видео + название. [Видео милые котики]\n'\
        '- Погода + город + страна. [Погода Киев Украина]\n'\
        '- Подбрось монетку.'
    
    await call.message.answer(text, disable_notification=True)


async def language_selector(call: types.callback_query):
    lang = str(call.data)
    db = Database()
    db.user_data_save(call['from']['id'], 'lang_tts', lang.split('_')[1])
    await call.message.answer('Сохранил', disable_notification=True)


async def sql_request_cmd(message: types.Message):
    db = Database()
    sql = (' '.join(message.text.split()[:8][1:]))
    if sql:
        result = db.sql_request(sql)
        if result:
            str = ''
            for item in result:
                str += f' {item}\n'
            await message.answer(str, disable_notification=True)
        else:
            await message.answer('[+]', disable_notification=True)    
    else:
        await message.answer(f"Commands format: /sql_cmd 'SQL command'")


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

    dp.register_message_handler(sql_request_cmd, commands=['sql_cmd'], user_id=OWNER)