from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

lang_select = InlineKeyboardMarkup()
ru = InlineKeyboardButton(text='Русский', callback_data='ru')
en = InlineKeyboardButton(text='English', callback_data='en')
ua = InlineKeyboardButton(text='Українська', callback_data='uk')
de = InlineKeyboardButton(text='Deutsch', callback_data='de')
es = InlineKeyboardButton(text='Español', callback_data='es')
pl = InlineKeyboardButton(text='Polski', callback_data='pl')
lang_select.add(ua,ru,en,de,es,pl)


lang_voice_inline = InlineKeyboardMarkup()
ru_voice = InlineKeyboardButton(text='Русский', callback_data='ru-RU')
ua_voice = InlineKeyboardButton(text='Українська', callback_data='uk-UA')
en_voice = InlineKeyboardButton(text='English', callback_data='en-US')
lang_voice_inline.add(en_voice, ua_voice, ru_voice)


cancel_inline = InlineKeyboardMarkup()
cancel = InlineKeyboardButton(text='Отмена', callback_data='cancel')
cancel_inline.add(cancel)

help_inline = InlineKeyboardMarkup()
help = InlineKeyboardButton(text='Что я умею?', callback_data='help')
help_inline.add(help)

listen_inline = InlineKeyboardMarkup()
listen = InlineKeyboardButton(text='Прослушать', callback_data='listen')
listen_inline.add(listen)