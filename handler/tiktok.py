from aiogram import types, Dispatcher
import os.path
from function.tiktok_download import *
import random

async def tk_video_sender(message : types.message):
    video_id = str(message['from']['id'])
    file_path = 'tiktok_download/'+str(video_id)+'.mp4'

    answer_list = ['Я сделяль!','Опять работа?!','Вам меня не жалко?','Пиво-это главный секрет альфа!','Давай напьемся!', \
        'Чего желает мой повелитель?','Да свершится предначертанное!','Интим и гербалайф не предлагать.','Вы меня смущаете.',\
        'хрю-хрю-хрю','Слава Україні!']

    download_video(str(message.text), video_id)
    await message.reply_video(open(file_path, 'rb'), caption=random.choice(answer_list))
    os.remove(file_path)

    
def handlers_tiktok(dp: Dispatcher):
    dp.register_message_handler(tk_video_sender, regexp='(https?:\/\/)?(vm.|www.)?(tiktok.com\/)')
    # dp.register_inline_handler(tk_video_sender)
