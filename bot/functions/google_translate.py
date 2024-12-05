from googletrans import Translator

def google_translate(src_text, dest_lang):
    try:
        translator = Translator()
        src_lang = translator.detect(src_text).lang
        if isinstance(src_lang, str):
            translated_text = translator.translate(src_text ,dest=dest_lang ,src=src_lang)
        else: 
            translated_text = translator.translate(src_text ,dest=dest_lang ,src=src_lang[0])
        return(translated_text.text)
    except: return('Введите коректный текст или свяжитесь с @ShtefanNein.')

def language_cheker(src_text):
    try:
        translator = Translator()
        src_lang = translator.detect(src_text).lang
        if isinstance(src_lang, str):
            return(src_lang)
        else:
            return(src_lang[0])
    except Exception as error: print(error)         
