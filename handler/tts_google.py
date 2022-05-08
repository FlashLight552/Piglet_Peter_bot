from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from gtts import gTTS
import os

from function.google_translate import language_cheker
from data.btn import cancel_inline


class Form(StatesGroup):
    tts = State()


async def tts_request(message : types.message):
    await message.answer('Напиши мне сообщение и я его озвучу', reply_markup=cancel_inline, disable_notification=True)
    await Form.tts.set()


async def get_tts(message : types.message, state: FSMContext):
    try:
        await types.ChatActions.record_voice()
        
        text = message.text
        lang = language_cheker(text)
        result = gTTS(text=text, lang=lang, slow=False)
        path = 'downloads/voice_message/'+str(message.message_id) + '_' + str(message.chat.id) + '.mp3'
        result.save(path) 
        
        await message.answer_voice(open(path, 'rb'), disable_notification=True)
        os.remove(path)
    except:
        await message.answer('Упс, техничиские проблемки. Возможно было использовано более одного языка, проверь сообщение или попробуйте еще раз. Если ничего не выходит - свяжитесь с @ShtefanNein.', disable_notification=True)        
    await state.finish()


def handlers_tts_google(dp: Dispatcher):
    dp.register_message_handler(tts_request, commands=['say'])
    dp.register_message_handler(get_tts, state=Form.tts)
