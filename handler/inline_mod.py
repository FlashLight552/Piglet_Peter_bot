from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQuery, InlineQueryResultCachedVoice, InlineQueryResultCachedVideo
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import hashlib    
from gtts import gTTS
import os
import re


from create_bot import telegram_bot
from data.config import FILES_STORAGE_GROUP
from function.tiktok_download import *

tiktok_pattern = re.compile('(https?:\/\/)?(vm.|www.)?(tiktok.com\/)')


async def inline_tts(inline_query: InlineQuery, state: FSMContext):
    text = inline_query.query or 'echo'
    description = 'Жми сюда для отправки.'
    if tiktok_pattern.match(text):
            video_id = inline_query.from_user.id
            file_path = 'downloads/tiktok/'+str(video_id)+'.mp4'
            download_video(text, video_id)
            storage = await telegram_bot.send_video(FILES_STORAGE_GROUP, open(file_path, 'rb'), disable_notification=True)
            try:
                os.remove(file_path)
            except:
                pass   
            result_id: str = hashlib.md5(text.encode()).hexdigest()
            item = InlineQueryResultCachedVideo(
                id=result_id,
                video_file_id=storage.video.file_id,
                title='TikTok',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Link', url=text)),
                description=description,
            )
            await inline_query.answer([item], cache_time=300)
    
    else:
        if text != 'echo':
            async with state.proxy() as proxy:
                if 'language' in proxy:
                    lang = proxy['language']
                else:
                    lang = 'ru'
            result = gTTS(text=text, lang=lang, slow=False)
            path = f'downloads/voice_message/{inline_query.id}_{inline_query.from_user.id}.mp3'
            result.save(path) 
            result_id: str = hashlib.md5(text.encode()).hexdigest()
            storage = await telegram_bot.send_voice(FILES_STORAGE_GROUP, open(path, 'rb'))
            os.remove(path)
            item = InlineQueryResultCachedVoice(
                title = description,
                id = result_id,
                voice_file_id = storage.voice.file_id,
            )
            await inline_query.answer([item], cache_time=300, switch_pm_text='Сменить язык', switch_pm_parameter='language')


def handlers_inline_mod(dp: Dispatcher):
    dp.register_inline_handler(inline_tts)