from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_inline = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Отмена', callback_data='cancel')
)

lang_select = InlineKeyboardMarkup(row_width=3).add(
    InlineKeyboardButton(text='Українська', callback_data='uk'),
    InlineKeyboardButton(text='Русский', callback_data='ru'),
    InlineKeyboardButton(text='English', callback_data='en'),
    InlineKeyboardButton(text='Deutsch', callback_data='de'),
    InlineKeyboardButton(text='Español', callback_data='es'),
    InlineKeyboardButton(text='Polski', callback_data='pl'),
)

lang_for_inline_tts = InlineKeyboardMarkup(row_width=3).add(
    InlineKeyboardButton(text='Українська', callback_data='inl_uk'),
    InlineKeyboardButton(text='Русский', callback_data='inl_ru'),
    InlineKeyboardButton(text='English', callback_data='inl_en'),
    InlineKeyboardButton(text='Deutsch', callback_data='inl_de'),
    InlineKeyboardButton(text='Español', callback_data='inl_es'),
    InlineKeyboardButton(text='Polski', callback_data='inl_pl'),
)


lang_voice_inline = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Українська', callback_data='uk-UA'),
    InlineKeyboardButton(text='English', callback_data='en-US'),
    InlineKeyboardButton(text='Русский', callback_data='ru-RU'),
)


help_inline = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Что я умею?', callback_data='help')
)

listen_inline = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Прослушать', callback_data='listen')
)


wait_inline = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Ожидайте', callback_data='wait')
)

ready_inline = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Готово', callback_data='ready')
)

translate_ask_inline = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Перевести?', callback_data='translate_ask')
)