from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineQuery, InlineQueryResultCachedVoice

import hashlib    
from gtts import gTTS
import os

from function.google_translate import language_cheker
from data.btn import cancel_inline

from create_bot import telegram_bot
from data.config import FILES_STORAGE_GROUP



class Form(StatesGroup):
    tts = State()

async def tts_request(message : types.message):
    await message.answer('Напиши мне сообщение и я его озвучу', reply_markup=cancel_inline, disable_notification=True)
    await Form.tts.set()

async def get_tts(message : types.message, state: FSMContext):
    try:
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


async def inline_tts(inline_query: InlineQuery, state: FSMContext):
    text = inline_query.query or 'echo'
    async with state.proxy() as proxy:
        if 'language' in proxy:
            lang = proxy['language']
        else:
            lang = 'ru'

    result = gTTS(text=text, lang=lang, slow=False)
    path = 'downloads/voice_message/'+str(inline_query.id) + '_' + str(inline_query.from_user.id) + '.mp3'
    result.save(path) 

    result_id: str = hashlib.md5(text.encode()).hexdigest()
    storage = await telegram_bot.send_voice(FILES_STORAGE_GROUP, open(path, 'rb'))
    os.remove(path)
    

    item = InlineQueryResultCachedVoice(
        title = 'Попизделкин 2.0',
        id = result_id,
        voice_file_id = storage.voice.file_id,

    )
    await inline_query.answer([item], cache_time=3, switch_pm_text='Сменить язык', switch_pm_parameter='language')
   


def handlers_tts_google(dp: Dispatcher):
    dp.register_message_handler(tts_request, commands=['say'])
    dp.register_message_handler(get_tts, state=Form.tts)
    dp.register_inline_handler(inline_tts)