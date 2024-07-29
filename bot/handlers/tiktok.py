from aiogram import types, Dispatcher
import os.path

from tiktok_downloader import snaptik, tikwm


async def tk_video_sender(message : types.Message):
    video_id = str(message['from']['id'])
    file_path = 'downloads/tiktok/'+str(video_id)

    await types.ChatActions.upload_document()
    try:
        snaptik(message.text)[0].download(file_path)
        await message.reply_video(open(file_path, 'rb'), disable_notification=True)
        os.remove(file_path)
        return
    except: pass

    try:
        tikwm(message.text)[0].download(file_path)
        await message.reply_video(open(file_path, 'rb'), disable_notification=True)
        os.remove(file_path)
        return
    except: return message.answer('This video is currently not available')


def handlers_tiktok(dp: Dispatcher):
    dp.register_message_handler(tk_video_sender, regexp='(https?:\/\/)?(vm.|www.|vt.)?(tiktok.com\/)')
