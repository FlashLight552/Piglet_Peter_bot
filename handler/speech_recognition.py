import subprocess
import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from aiogram import types, Dispatcher
from create_bot import telegram_bot
from function.google_recognize import google_rec
from function.vosk_ffmpeg import vosk_ffmpeg_model

from data.btn import *


async def voice_message(message:types.message, state: FSMContext):
    async with state.proxy() as proxy:
        if 'message_id_sr' in proxy:
            try:
                await telegram_bot.delete_message(proxy['chat_id_sr'], proxy['message_id_sr'])
                os.remove(proxy['file_path_sr']+'.oga')  
            except: pass   
    
        msg = await message.reply('На каком языке говорят?', reply_markup=lang_voice_inline, disable_notification=True)
        # download voice message
        file_id = message.voice.file_id
        file = await telegram_bot.get_file(file_id)
        file_path = file.file_path
        await telegram_bot.download_file(file_path, 'voice_message/'+str(file.file_id)+'.oga')
        
        proxy['file_path_sr'] = 'voice_message/'+str(file.file_id)
        proxy['message_id_sr'] = msg.message_id
        proxy['chat_id_sr'] = msg.chat.id


async def sel_lang_and_recog(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['data_sr'] = call.data
    
    src_filename = proxy['file_path_sr']+'.oga' 
    dest_filename = proxy['file_path_sr']+'.wav' 
    sample_rate=16000
    
    subprocess.run(['ffmpeg', '-i', src_filename,'-ar', str(sample_rate), '-ac', '1', '-af', 'highpass=f=200, lowpass=f=3000', dest_filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    result = ''
    error_text = 'Я не понимаю! Говорите текст четко в микрофон. Или свяжитесь с @ShtefanNein.'

    try : 
        result = google_rec(dest_filename, proxy['data_sr'])
        
    except Exception as error: print(error)      
        
    if not result:
        try : 
            result = vosk_ffmpeg_model(src_filename, proxy['data_sr'])
            
        except Exception as error: print(error)  
    if not result:        
        result = error_text

    # Message send
    await call.message.delete()  
    if result != error_text:   
        await call.message.answer(result, reply_markup=translate_ask_inline, disable_notification=True)
    else:
        await call.message.answer(result, disable_notification=True)    
    
    # Очистка
    try: 
        os.remove(proxy['file_path_sr']+'.oga')
        os.remove(proxy['file_path_sr']+'.wav')
    except: pass


async def translate_recog_text(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('На какой язык будем переводить?', reply_markup=lang_select, disable_notification=True)
    async with state.proxy() as proxy:
        proxy['call.message.text'] = call.message.text
    # await call.message.edit_text(proxy['call.message.text'], reply_markup=ready_inline)  
    await call.message.edit_text(proxy['call.message.text'], reply_markup=None)  


def handlers_sr(dp: Dispatcher):
    dp.register_message_handler(voice_message, content_types=['voice'])  
    
    dp.register_callback_query_handler(sel_lang_and_recog, text='ru-RU')
    dp.register_callback_query_handler(sel_lang_and_recog, text='uk-UA')
    dp.register_callback_query_handler(sel_lang_and_recog, text='en-US')

    dp.register_callback_query_handler(translate_recog_text, text='translate_ask')