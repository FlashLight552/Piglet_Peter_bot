from aiogram import Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultCachedVoice, InlineQueryResultCachedVideo
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import hashlib    
from gtts import gTTS
import os
import re


from config.create_bot import telegram_bot
from config.config import FILES_STORAGE_GROUP
from functions.tiktok_download import *
from functions.sql import Database


tiktok_pattern = re.compile('(https?:\/\/)?(vm.|www.)?(tiktok.com\/)')


async def inline_tts(inline_query: InlineQuery):
    text = inline_query.query or 'echo'
    description = 'Жми сюда для отправки.'
    db = Database()

    if tiktok_pattern.match(text):
            url = text.split('?')[0]
            video_id = inline_query.from_user.id
            file_path = 'downloads/tiktok/'+str(video_id)+'.mp4'
            download_video(url, video_id)
            storage = await telegram_bot.send_video(FILES_STORAGE_GROUP, open(file_path, 'rb'), disable_notification=True)
            try:
                os.remove(file_path)
            except:
                pass
            result_id: str = hashlib.md5(url.encode()).hexdigest()
            item = InlineQueryResultCachedVideo(
                id=result_id,
                video_file_id=storage.video.file_id,
                title='TikTok',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Link', url=url)),
                description=description,
            )
            await inline_query.answer([item], cache_time=300)
    
    else:
        if text != 'echo':
            with db.connection:
                lang = db.user_data_request(inline_query.from_user.id, 'lang_tts')
            if not lang:
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
            await inline_query.answer([item], cache_time=300, switch_pm_text='Сменить язык', switch_pm_parameter='language', is_personal=True)


def handlers_inline_mod(dp: Dispatcher):
    dp.register_inline_handler(inline_tts)