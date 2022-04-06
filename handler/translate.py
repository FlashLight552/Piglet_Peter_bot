from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text



from create_bot import telegram_bot
from data.btn import lang_select, cancel_inline
from func.google_trans import google_translate


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
        await message.answer(text)
    await telegram_bot.delete_message(proxy['chat_id'], proxy['massage_id'])    
    await state.finish()



# Регистрация хендлеров
def handlers_translate(dp: Dispatcher):
    dp.register_callback_query_handler(lang_choise, text='ru')
    dp.register_callback_query_handler(lang_choise, text='en')
    dp.register_callback_query_handler(lang_choise, text='uk')
    dp.register_callback_query_handler(lang_choise, text='de')
    dp.register_callback_query_handler(lang_choise, text='es')
    dp.register_callback_query_handler(lang_choise, text='pl')
    
    dp.register_callback_query_handler(cancel, text='cancel', state="*")
    
    dp.register_message_handler(message_answer, commands=['translate'])
    dp.register_message_handler(message_answer, Text(equals = 'Перевод', ignore_case = True))

    # dp.register_message_handler(cancel, state="*", commands='cancel')
    # dp.register_message_handler(cancel, Text(equals = 'Отмена', ignore_case = True), state="*" )
    dp.register_message_handler(translate, state=Form.text_message)
