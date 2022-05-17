import os
import glob

from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher

from config.create_bot import telegram_bot
from functions.sp_recognition import recognition
from functions.voice_assistant import assistant
from functions.sql import Database
from config.btn import *



async def voice_message(message:types.message, state: FSMContext):
    async with state.proxy() as proxy:
        if 'message_id_sr' in proxy:
            try:
                await telegram_bot.delete_message(proxy['chat_id_sr'], proxy['message_id_sr'])
                os.remove(proxy['file_path_sr']+'.oga')  
            except: pass   

        file_id = message.voice.file_id
        duration = message.voice.duration
        file = await telegram_bot.get_file(file_id)
        file_path = file.file_path
        await telegram_bot.download_file(file_path, 'downloads/voice_message/'+str(file.file_id)+'.oga')
        proxy['file_path_sr'] = 'downloads/voice_message/'+str(file.file_id)

        db = Database()
        lang = db.user_data_request(message.from_user.id, 'lang_assistant')
        if not lang:
            lang = 'ru-RU'

        src_filename = proxy['file_path_sr']+'.oga'
        dest_filename = proxy['file_path_sr']+'.wav'
        
        text = 'На каком языке говорят? Или воспользуйся функцией распознавания музыки Shazam.'
        
        if duration < 5:
            recog_result = recognition(src_filename,dest_filename,lang)
            assistent_result = assistant(message.from_user.id, recog_result)
            
            if assistent_result:
                voice_files = glob.glob(proxy['file_path_sr']+'.*')
                for item in voice_files:
                    os.remove(item)
                await message.answer(assistent_result, disable_notification=True, parse_mode = types.ParseMode.HTML)

            else:
                msg = await message.reply(text, reply_markup=lang_select_for_voice_message, disable_notification=True)
                proxy['message_id_sr'] = msg.message_id
                proxy['chat_id_sr'] = msg.chat.id
        
        else:
            msg = await message.reply(text, reply_markup=lang_select_for_voice_message, disable_notification=True)
            proxy['message_id_sr'] = msg.message_id
            proxy['chat_id_sr'] = msg.chat.id


async def sel_lang_and_recog(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['data_sr'] = call.data

    src_filename = proxy['file_path_sr']+'.oga'
    dest_filename = proxy['file_path_sr']+'.wav'

    result = recognition(src_filename,dest_filename,proxy['data_sr'])
    voice_files = glob.glob(proxy['file_path_sr']+'.*')

    for item in voice_files:
        os.remove(item)

    if result:
        await call.message.answer(result, reply_markup=translate_ask_inline, disable_notification=True)
    else:
        error_text = 'Я не понимаю! Говорите текст четко в микрофон. Или свяжитесь с @ShtefanNein.'
        await call.message.answer(error_text, disable_notification=True)


async def translate_recog_text(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.answer('На какой язык будем переводить?', reply_markup=lang_select_for_translate, disable_notification=True)
    async with state.proxy() as proxy:
        proxy['message_text'] = call.message.text
        proxy['chat_id'] = msg.chat.id
        proxy['message_id'] = msg.message_id

    await call.message.edit_text(proxy['message_text'], reply_markup=ready_inline)  


def handlers_sr(dp: Dispatcher):
    dp.register_message_handler(voice_message, content_types=['voice'])  
    
    dp.register_callback_query_handler(sel_lang_and_recog, text='ru-RU')
    dp.register_callback_query_handler(sel_lang_and_recog, text='uk-UA')
    dp.register_callback_query_handler(sel_lang_and_recog, text='en-US')
    
    dp.register_callback_query_handler(translate_recog_text, text='translate_ask')