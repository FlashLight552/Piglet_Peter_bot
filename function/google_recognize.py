import speech_recognition as sr

def google_rec(dest_filename, lang):
    r = sr.Recognizer()
    with sr.AudioFile(dest_filename) as source:
        audio = r.record(source) 
        r.adjust_for_ambient_noise(source)
        text = r.recognize_google(audio, language=lang)
        return(text)