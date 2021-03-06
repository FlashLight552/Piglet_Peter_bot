from aiogram import types, Dispatcher
import os.path
from functions.tiktok_download import *


async def tk_video_sender(message : types.message):
    video_id = str(message['from']['id'])
    file_path = 'downloads/tiktok/'+str(video_id)+'.mp4'

    await types.ChatActions.upload_video()
    download_video(str(message.text), video_id)
    await message.reply_video(open(file_path, 'rb'), disable_notification=True)
    os.remove(file_path)


def handlers_tiktok(dp: Dispatcher):
    dp.register_message_handler(tk_video_sender, regexp='(https?:\/\/)?(vm.|www.)?(tiktok.com\/)')
