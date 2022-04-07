from vosk import Model, KaldiRecognizer, SetLogLevel
import subprocess
import json

def vosk_ffmpeg_ru_model(src_filename, model):
    SetLogLevel(-1)

    sample_rate=16000
    model = Model("models/"+model)
    rec = KaldiRecognizer(model, sample_rate)
    

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