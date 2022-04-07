from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from gtts import gTTS
import os


from create_bot import telegram_bot
from data.btn import lang_select, cancel_inline, listen_inline
from function.google_translate import google_translate, language_cheker


# Класс состояний
class Form(StatesGroup):
    text_message = State()


async def message_answer(message: types.message):
    await message.answer('На какой язык будем переводить?', reply_markup=lang_select) 


async def lang_choise(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['data'] = call.data
        
        msg = await call.message.answer('Что я должен перевести?', reply_markup=cancel_inline)
        proxy['massage_id'] = msg.message_id
        proxy['chat_id'] = msg.chat.id

    await Form.text_message.set() # Устанавливаем состояние   


async def cancel(call: types.CallbackQuery, state: FSMContext):
    current_stage = await state.get_state()
    if current_stage is None:
        return
    await call.message.delete()   
    await state.finish() # Выключаем состояние 


async def translate(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        text = google_translate(message.text, dest_lang=proxy['data'])
        await message.answer(text, reply_markup=listen_inline)
    await telegram_bot.delete_message(proxy['chat_id'], proxy['massage_id'])    
    await state.finish()


async def listen(call: types.CallbackQuery):
    try:
        text = call.message.text
        lang = language_cheker(text)
        result = gTTS(text=text, lang=lang, slow=False)
        path = 'voice_message/'+str(call.message.message_id) + '_' + str(call.message.chat.id) + '.mp3'
        result.save(path) 
        await call.message.answer_voice(open(path, 'rb'))
        os.remove(path)
    except : call.message.answer('Упс, техничиские проблемки. Свяжитесь с @ShtefanNein.')


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
    
    dp.register_message_handler(message_answer, commands=['translate'])
    dp.register_message_handler(message_answer, Text(equals = 'Перевод', ignore_case = True))

    dp.register_message_handler(translate, state=Form.text_message)
