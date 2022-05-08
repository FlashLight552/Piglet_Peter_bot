from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from gtts import gTTS
import os

from function.google_translate import google_translate, language_cheker
from create_bot import telegram_bot
from data.btn import *



async def message_question(message: types.message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['message_text'] = message.text
        msg = await message.answer('На какой язык будем переводить?', reply_markup=lang_select, disable_notification=True) 
        proxy['chat_id'] = msg.chat.id
        proxy['message_id'] = msg.message_id


async def lang_choise(call: types.CallbackQuery, state: FSMContext):
    await types.ChatActions.typing()
    async with state.proxy() as proxy:
        text = google_translate(proxy['message_text'], dest_lang=call.data)
        await telegram_bot.edit_message_text(chat_id=proxy['chat_id'],message_id=proxy['message_id'],
                                        text = text, reply_markup=listen_inline)
        
     

async def listen(call: types.CallbackQuery):
    await types.ChatActions.record_voice()
    try:
        text = call.message.text
        await call.message.edit_text(text, reply_markup=wait_inline)
        lang = language_cheker(text)
        result = gTTS(text=text, lang=lang, slow=False)
        path = 'downloads/voice_message/'+str(call.message.message_id) + '_' + str(call.message.chat.id) + '.mp3'
        result.save(path) 
        await call.message.answer_voice(open(path, 'rb'), disable_notification=True)
        os.remove(path)
        await call.message.edit_text(text, reply_markup=ready_inline)
    except : 
        await call.message.answer('Упс, техничиские проблемки. Свяжитесь с @ShtefanNein.', disable_notification=True)
        await call.message.edit_text(text, reply_markup=ready_inline)


async def cancel(call: types.CallbackQuery, state: FSMContext):
    current_stage = await state.get_state()
    if current_stage is None:
        return
    await call.message.delete()   
    await state.finish() 


# Регистрация хендлеров
def handlers_translate(dp: Dispatcher):
    dp.register_callback_query_handler(lang_choise, text='ru')
    dp.register_callback_query_handler(lang_choise, text='en')
    dp.register_callback_query_handler(lang_choise, text='uk')
    dp.register_callback_query_handler(lang_choise, text='de')
    dp.register_callback_query_handler(lang_choise, text='es')
    dp.register_callback_query_handler(lang_choise, text='pl')

    dp.register_callback_query_handler(listen, text='listen')
    dp.register_callback_query_handler(cancel, text='cancel', state="*")
    
    dp.register_message_handler(message_question, chat_type='private')
