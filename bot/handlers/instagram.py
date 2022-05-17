from aiogram import types, Dispatcher
from functions.instagram import instagram_downloader
import glob
import os

async def inst_dl(message: types.Message):
    msg = await message.answer('Загрузка поста.', disable_notification=True)
    await types.ChatActions.upload_document()

    file = instagram_downloader(message.text)
    
    if file.startswith('Login error:') or file.startswith('Access denied:'):
        await msg.edit_text(file, disable_notification=True)
    
    else:
        await types.ChatActions.upload_document()
        file_jpg = glob.glob(fr'downloads/instagram/{file}*.jpg')
        file_mp4 = glob.glob(fr'downloads/instagram/{file}*.mp4') 
        media = types.MediaGroup()
        
        if file_jpg:
            for item in file_jpg:
                media.attach_photo(open(item, 'rb'))

        if file_mp4:
            for item in file_mp4:
                media.attach_video(open(item, 'rb'))                        
        
        await message.reply_media_group(media, disable_notification=True)
        await msg.delete()   

        for item in glob.glob(fr'downloads/instagram/{file}*'):
            os.remove(item)
 
def intdl_hendler(dp: Dispatcher):
    dp.register_message_handler(inst_dl, regexp='(https?:\/\/)?(www.)?(instagram.com\/)')

