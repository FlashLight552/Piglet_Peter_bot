from aiogram import types, Dispatcher
import os.path

from func.tiktok_func import *


# async def tk_video_sender(message : types.message):
#     # video_id = get_video_id(message.text)
#     video_id = str(message['from']['id'])
#     file_path = 'tiktok_download/'+str(video_id)+'.mp4'
#     print('Готовлюсь качать')
#     download_video(str(message.text), video_id)
#     print('скачал')
#     await message.answer('Отправляю видео, ожидайте')
#     await message.answer_video(open(file_path, 'rb'))
#     os.remove(file_path)

async def tk_video_sender(message : types.message):
    video_id = str(message['from']['id'])
    # file_path = 'tiktok_download/'+str(video_id)+'.mp4'
    print('Готовлюсь качать')
    download_video(str(message.text), video_id)
    print('скачал')



def handlers_tiktok(dp: Dispatcher):
    dp.register_message_handler(tk_video_sender, regexp='(https?:\/\/)?(vm.|www.)?(tiktok.com\/)')
    # dp.register_inline_handler(tk_video_sender)

