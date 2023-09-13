from aiogram import types, Dispatcher
import os.path
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
        for num, item in enumerate(download_list):
            if len(download_list)-1 != num:
                media.attach_photo(types.InputFile(item))
        await message.reply_media_group(media=media, disable_notification=True)
        await message.reply_audio(open(download_list[len(download_list)-1], 'rb'), disable_notification=True, title='audio') 

        for item in download_list:
            os.remove(item)
        return
    
    await message.reply_video(open(download_list[0], 'rb'), disable_notification=True)
    os.remove(download_list[0])


def handlers_tiktok(dp: Dispatcher):
    dp.register_message_handler(tk_video_sender, regexp='(https?:\/\/)?(vm.|www.|vt.)?(tiktok.com\/)')
