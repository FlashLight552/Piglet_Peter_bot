from aiogram import types, Dispatcher
import os.path
import asyncio
from functions.tiktok_download import *


async def tk_video_sender(message : types.Message):
    video_id = str(message['from']['id'])
    file_path = 'downloads/tiktok/'+str(video_id)

    td = tiktok_downloader()
    await types.ChatActions.upload_document()
    try:
        download_list = td.musicaldown(str(message.text), file_path)
    except: return message.answer('This video is currently not available')

    if len(download_list) > 1:
        media = types.MediaGroup()
        iter_num = 0
        for num, item in enumerate(download_list):
            await types.ChatActions.upload_photo()
            if len(download_list)-1 != num:
                if iter_num < 10:
                    media.attach_photo(types.InputFile(item))
                    iter_num += 1
                else:
                    iter_num = 1
                    await asyncio.sleep(5)
                    await message.answer_media_group(media=media, disable_notification=True)
                    media = types.MediaGroup()
                    media.attach_photo(types.InputFile(item))
                    
        await asyncio.sleep(5)
        await message.answer_media_group(media=media, disable_notification=True)
        await types.ChatActions.upload_audio()
        await asyncio.sleep(5)
        await message.reply_audio(open(download_list[len(download_list)-1], 'rb'), disable_notification=True, title='audio') 

        for item in download_list:
            os.remove(item)
        return
    
    await message.reply_video(open(download_list[0], 'rb'), disable_notification=True)
    os.remove(download_list[0])


def handlers_tiktok(dp: Dispatcher):
    dp.register_message_handler(tk_video_sender, regexp='(https?:\/\/)?(vm.|www.|vt.)?(tiktok.com\/)')
