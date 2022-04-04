import subprocess
import os


from aiogram import types, Dispatcher
from create_bot import telegram_bot
from func.google_recognize import google_rec
from func.vosk_offline import vosk_ru_model

async def voice_message(message:types.message):
    # download voice message
    file_id = message.voice.file_id
    file = await telegram_bot.get_file(file_id)
    file_path = file.file_path
    await telegram_bot.download_file(file_path, 'voice_message/'+str(file.file_id)+'.oga')
   
    # oga to wav
    src_filename = 'voice_message/'+str(file.file_id)+'.oga' 
    dest_filename = 'voice_message/'+str(file.file_id)+'.wav' 
    subprocess.run(['ffmpeg', '-i', src_filename, dest_filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try : result = google_rec(dest_filename)
    except: result = vosk_ru_model(dest_filename)

    # Message send
    try: await message.reply(result)
    except: await message.reply('СЛОЖНА, СЛОЖНА, НИЧЕГО НЕ ПОНЯТНО, СЛОЖНА!')    

    
    # Очистка
    try: 
        os.remove('voice_message/'+file.file_id+'.oga')
        os.remove('voice_message/'+file.file_id+'.wav')
    except: pass
def handlers_sr(dp: Dispatcher):
    dp.register_message_handler(voice_message, content_types=['voice'])  