from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from functions.animego_parser import *
from functions.sql import Database

async def anime_by_url(message: types.message):
    r = request_anime_info(message.text)
    title = f'{r[0]}\n'
    poster = f'{r[1]}'
    status = f'Статус: {r[2]}\n' if r[2]!= '' else ''
    amount_ep = f'Количество эпизодов: {r[3]}\n' if r[3]!= '' else ''
    next_ep = f'Следующий эпизод: {r[4]}\n' if r[4]!= '' else ''
    dub = f'Озвучка: {r[5]}\n'  if r[5]!= '' else ''
    sub = ''
    
    db = Database()
    with db.connection:
        sub_dub_list = db.select_dub_from_sub_to_title(message.from_user.id, title.strip())
    
    if r[2] == 'Онгоинг':
        sub = '\nПодписаться на получение уведомления о новой серии в твоей любимой озвучке.'
        dub_studio = str(r[5]).split(',')

        inline_select_dub = InlineKeyboardMarkup()
        for item in dub_studio:
            if item.strip() in sub_dub_list:
                text = f'✅ {item.strip()}'
                callback_data = f'dub_studio+{str(item).strip()}+y'
            else:
                text = f'❌ {item.strip()}' 
                callback_data = f'dub_studio+{str(item).strip()}+n'  
            inline_select_dub.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    caption = f'{title}{status}{amount_ep}{next_ep}{dub}{sub}'.strip()
    if 'inline_select_dub' in locals():
        await message.answer_photo(poster, caption = caption, reply_markup = inline_select_dub)
    else:
        await message.answer_photo(poster, caption = caption)

async def callback_kb_sub(call: types.CallbackQuery):
    dub_studio = str(call.data).split('+')[1].strip()
    did_subscribed = str(call.data).split('+')[2].strip()
    title_name = str(call.message.caption).split('\n')[0]
    user_id = call.from_user.id
    sub_dub_list = []

    db = Database()
    with db.connection:
        try:
            if did_subscribed == 'n':
                db.sub_to_new_release(user_id, title_name, dub_studio)
            else:
                db.unsub_from_new_release(user_id,title_name,dub_studio)
            sub_dub_list = db.select_dub_from_sub_to_title(user_id, title_name)
        except: pass
    
    dub_list = []
    kb = call.message.reply_markup
    edited_kb = str(kb).replace('[','').replace(']','').replace('{','').replace('}','').replace('"inline_keyboard":', '').split(',')
    for item in edited_kb:
        if item.split('": "')[0] == ' "text':
            dub_list.append(item.split('": "')[1].replace('"','').replace('❌ ','').replace('✅ ',''))
    
    inline_select_dub = InlineKeyboardMarkup()
    for item in dub_list:
        if item in sub_dub_list:
            text = f'✅ {item}'
            callback_data = f'dub_studio+{item}+y'
        else:
            text = f'❌ {item}' 
            callback_data = f'dub_studio+{item}+n' 
        inline_select_dub.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    await call.message.edit_reply_markup(reply_markup=inline_select_dub)

def handlers_anime(dp: Dispatcher):
    dp.register_message_handler(anime_by_url, regexp='(https?:\/\/)?(animego.org\/)')
    dp.register_callback_query_handler(callback_kb_sub, regexp='(dub_studio)')