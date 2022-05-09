from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext

import os
from shazamio import Shazam
from youtube_search import YoutubeSearch

from config.btn import wait_inline


async def shazam_recog(src_filename):
    shazam = Shazam()
    out = await shazam.recognize_song(src_filename)
    lyrics = ''
    try: 
        title = out['track']['title']
        subtitle = out['track']['subtitle']
        images = out['track']['images']['coverart']
        try:
            for item in out['track']['sections']:
                if item['type'] == 'LYRICS':
                    for text in item['text']:
                        lyrics += f'{text}\n'
        except:
            lyrics = 'empty'
    
        result = YoutubeSearch(f'{subtitle} {title}', max_results=1).to_dict()
        for item in result:
            id = item['id']
            yt_url = f'https://www.youtube.com/watch?v={id}'
        return subtitle,title,images,yt_url,lyrics
    except:
        subtitle = title = images = yt_url = lyrics = 'empty'
        return subtitle,title,images,yt_url,lyrics

 
async def shazam_serch_by_recog(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(call.message.text, reply_markup=wait_inline)
    await types.ChatActions.typing()

    async with state.proxy() as proxy:
        src_filename = proxy['file_path_sr']+'.oga'
        subtitle,title,images,yt_url,lyrics = await shazam_recog(src_filename)
        
        if subtitle != 'empty':
            proxy['lyrics'] = lyrics
            if lyrics != 'empty':
                await call.message.answer_photo(images, caption=f'{subtitle} {title}', reply_markup=InlineKeyboardMarkup().add(
                                                                    InlineKeyboardButton(text='Youtube', url=yt_url),
                                                                    InlineKeyboardButton(text='Lyrics', callback_data='lyrics')))
            else:
                await call.message.answer_photo(images, caption=f'{subtitle} {title}', reply_markup=InlineKeyboardMarkup().add(
                                                                    InlineKeyboardButton(text='Youtube', url=yt_url)))
                                                                    
            await call.message.delete()
            os.remove(src_filename)
        else:
            await call.message.edit_text('Я ничего не нашел, попробуй еще раз.', reply_markup=None)  
            os.remove(src_filename)


async def lyrics(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
       lyrics = proxy['lyrics']
    await call.message.answer(lyrics)


def handlers_shazam(dp: Dispatcher):
    dp.register_callback_query_handler(shazam_serch_by_recog, text='shazam')
    dp.register_callback_query_handler(lyrics, text='lyrics')