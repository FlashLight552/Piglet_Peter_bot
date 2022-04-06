from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

lang_select = InlineKeyboardMarkup()
ru = InlineKeyboardButton(text='Русский', callback_data='ru')
en = InlineKeyboardButton(text='English', callback_data='en')
ua = InlineKeyboardButton(text='Українська', callback_data='uk')
de = InlineKeyboardButton(text='Deutsch', callback_data='de')
es = InlineKeyboardButton(text='Español', callback_data='es')
pl = InlineKeyboardButton(text='Polski', callback_data='pl')
lang_select.add(ua,ru,en,de,es,pl)


cancel_inline = InlineKeyboardMarkup()
cancel = InlineKeyboardButton(text='Отмена', callback_data='cancel')
cancel_inline.add(cancel)

help_inline = InlineKeyboardMarkup()
help = InlineKeyboardButton(text='Что я умею?', callback_data='help')
help_inline.add(help)
