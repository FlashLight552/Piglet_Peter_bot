import wave
from vosk import Model, KaldiRecognizer
from vosk import SetLogLevel

import json    
    
def vosk_ru_model(dest_filename):    
    # vosk start recog 
    # SetLogLevel(-1)
    wf = wave.open(dest_filename, "rb")

    # initialize a str to hold results
    results = ""

    # build the model and recognizer objects.
    
    model = Model("models/vosk-model-small-ru-0.22")


    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)
    recognizer.SetMaxAlternatives(10)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            recognizerResult = json.loads(recognizer.Result())
            print(recognizerResult)
            results = results + ' ' + recognizerResult['text']
    # print(results)
    return(results)