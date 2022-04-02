import speech_recognition as sr  
# from pydub import AudioSegment
# import soundfile as sf

from aiogram import types, Dispatcher
from create_bot import telegram_bot




async def voice_message(message:types.message):
    # download voice message
    file_id = message.voice.file_id
    file = await telegram_bot.get_file(file_id)
    file_path = file.file_path
    await telegram_bot.download_file(file_path, "voice_message/voice_message.ogg")

    # data, samplerate = sf.read('voice_message/voice_message.ogg')
    # sf.write('voice_message/voice_message.wav', data, samplerate)

    # start recornize
    r = sr.Recognizer()
    audio_source = sr.AudioFile('voice_message/voice_message.ogg')
    with audio_source as source:
        audio = r.record(source)
        r.recognize_google(audio)
        


def handlers_sr(dp: Dispatcher):
    dp.register_message_handler(voice_message, content_types=['voice'])  