from googletrans import Translator

def google_translate(src_text, dest_lang):
    try:
        translator = Translator()
        src_lang = translator.detect(src_text)
        translated_text = translator.translate(src_text ,dest=dest_lang ,src=src_lang.lang)
        return(translated_text.text)
    except: return('Введите коректный текст или свяжитесь с @ShtefanNein.')

# print(google_translate('Some text', 'ru'))