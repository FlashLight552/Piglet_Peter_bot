import speech_recognition as sr

def google_rec(dest_filename):
    r = sr.Recognizer()
    with sr.AudioFile(dest_filename) as source:
        audio = r.record(source)  # read the entire audio file
        r.adjust_for_ambient_noise(source)
        text = r.recognize_google(audio, language='ru-Ru')
        # text = r.recognize_wit(audio, key='R5KUOKEUQY6MOKLTJPYQQEQFKEDWDPUH')



        return(text)