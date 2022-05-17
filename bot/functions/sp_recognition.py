import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel

import subprocess
import json


def google_ffmpeg_model(src_filename:str, dest_filename:str, lang:str) -> str:
    
    """
    src_filename : oga file
    dest_filename : waw file
    lang: language
    """
    sample_rate=16000
    subprocess.run(['ffmpeg', '-n', '-i', src_filename,'-ar', str(sample_rate), 
                    '-ac', '1', '-af', 'highpass=f=200, lowpass=f=3000', 
                    dest_filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    r = sr.Recognizer()
    with sr.AudioFile(dest_filename) as source:
        audio = r.record(source) 
        r.adjust_for_ambient_noise(source)
        text = r.recognize_google(audio, language=lang)
        return(text)


def vosk_ffmpeg_model(src_filename:str, lang:str) -> str:
    
    """
    src_filename : oga file
    lang: language
    """
    
    SetLogLevel(-1)

    sample_rate=16000
    lang = Model("models/"+lang)
    rec = KaldiRecognizer(lang, sample_rate)
    

    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                src_filename,
                                '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                                stdout=subprocess.PIPE)

    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if not rec.AcceptWaveform(data):
            result = (json.loads(rec.PartialResult()))

    return(result['partial'])


def recognition(src_filename:str, dest_filename:str, lang:str) -> str:
    """
    src_filename : oga file
    dest_filename : waw file
    lang: language
    """
    try:
        return google_ffmpeg_model(src_filename, dest_filename, lang)
    except: 
        try:
            return vosk_ffmpeg_model(src_filename, lang)
        except: 
            return 

 