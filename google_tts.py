from gtts import gTTS


mytext = 'Итак, первый тест перевода текста в голосовое сообщение'
language = 'ru'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("welcome.mp3")