import subprocess
import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from aiogram import types, Dispatcher
from create_bot import telegram_bot
from function.google_recognize import google_rec
from function.vosk_ffmpeg import vosk_ffmpeg_ru_model

from data.btn import *

# Класс состояний
class Form(StatesGroup):
    voice_recog = State()


async def voice_message(message:types.message, state: FSMContext):
    await message.reply('На каком языке говорят?', reply_markup=lang_voice_inline)
    # download voice message
    file_id = message.voice.file_id
    file = await telegram_bot.get_file(file_id)
    file_path = file.file_path
    await telegram_bot.download_file(file_path, 'voice_message/'+str(file.file_id)+'.oga')
    
    async with state.proxy() as proxy:
        proxy['file_path'] = 'voice_message/'+str(file.file_id)
    await Form.voice_recog.set()


async def sel_lang_and_recog(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['data'] = call.data

    src_filename = proxy['file_path']+'.oga' 
    dest_filename = proxy['file_path']+'.wav' 
    sample_rate=16000

    subprocess.run(['ffmpeg', '-i', src_filename,'-ar', str(sample_rate), '-ac', '1', '-af', 'highpass=f=200, lowpass=f=3000', dest_filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try : result = google_rec(dest_filename, proxy['data'])
    except: 
        try : result = vosk_ffmpeg_ru_model(src_filename, proxy['data'])
        except: result = 'Я не понимаю! Говорите текст четко в микрофон. Или свяжитесь с @ShtefanNein.'

        # Message send
    await call.message.delete()    
    await call.message.answer(result, reply_markup=translate_ask_inline)
    
    # Очистка
    try: 
        os.remove(proxy['file_path']+'.oga')
        os.remove(proxy['file_path']+'.wav')
    except: pass

    await state.finish()


async def translate_recog_text(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('На какой язык будем переводить?', reply_markup=lang_select)
    async with state.proxy() as proxy:
        proxy['call.message.text'] = call.message.text
    # await call.message.edit_text(proxy['call.message.text'], reply_markup=ready_inline)  
    await call.message.edit_text(proxy['call.message.text'], reply_markup=None)  

def handlers_sr(dp: Dispatcher):
    dp.register_message_handler(voice_message, content_types=['voice'])  
    dp.register_callback_query_handler(sel_lang_and_recog, text='ru-RU', state=Form.voice_recog)
    dp.register_callback_query_handler(sel_lang_and_recog, text='uk-UA', state=Form.voice_recog)
    dp.register_callback_query_handler(sel_lang_and_recog, text='en-US', state=Form.voice_recog)

    dp.register_callback_query_handler(translate_recog_text, text='translate_ask')