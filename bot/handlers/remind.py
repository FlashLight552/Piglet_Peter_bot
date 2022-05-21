from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from config.config import WEBAPPS_URL
from functions.sql import Database
from timezonefinder import TimezoneFinder


async def remind_start_app(message: types.Message):
    db = Database()
    timezone_db = db.user_data_request(message.from_user.id, 'tz')
    if timezone_db:
        await message.answer('Заполни форму для создания напоминания',
                    reply_markup=InlineKeyboardMarkup().add(
                        InlineKeyboardButton(text='Тыкни сюда', 
                        web_app=WebAppInfo(url=f"{WEBAPPS_URL}"))))

    else:
        await message.answer('Сначала отправь мне свою геолокацию,'\
                            ' чтоб я мог определить твой часовой пояс.')

async def get_loc(message: types.Message):
    await message.delete()
    latitude = message.location.latitude
    longitude = message.location.longitude
    
    tf = TimezoneFinder()
    tz = tf.timezone_at(lng=longitude, lat=latitude)    

    db = Database()
    db.user_data_save(message.from_user.id, 'tz', tz)

    await message.answer(f'Геолокация: {tz}\n',
            reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(text='Напомни мне', 
            web_app=WebAppInfo(url=f"{WEBAPPS_URL}")))) 


def handlers_remind(dp: Dispatcher):
    dp.register_message_handler(remind_start_app, commands=['remind_me'])
    dp.register_message_handler(get_loc, content_types=['location'])