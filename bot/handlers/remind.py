from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from config.config import WEBAPPS_URL

async def remind_start_app(message: types.Message):
    await message.answer('Заполни форму для создиния напоминания',
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(text='Тыкни сюда', 
                    web_app=WebAppInfo(url=f"{WEBAPPS_URL}"))))


def handlers_remind(dp: Dispatcher):
    dp.register_message_handler(remind_start_app, commands=['remind_me'])