from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,  ReplyKeyboardRemove

from pyowm.utils.config import get_default_config

import pyowm
import os

config_dict = get_default_config()
config_dict['language'] = 'ru' 

owm = pyowm.OWM('778da4a75335bc96792e7075b5831234', config_dict)
mgr = owm.weather_manager()

observation = mgr.weather_at_place('Krasnodar, RU')
w = observation.weather

temp_temperature = w.temperature('celsius')['temp']
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот вышел в онлайн')

#@dp.message_handler(commands=['start', 'help'])
#async def command_start(messange : types.Message):
    #await bot.send_message(message.from_user.id, w)
#@dp.message_handler(commands==['start']):


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["🌡Погода🌡", "🌧Осадки🌧"]
    keyboard.add(*buttons)
    await message.answer("Что вы хотите узнать?", reply_markup=keyboard)

@dp.message_handler(Text(equals="🌡Погода🌡"))
async def weather(message: types.Message):
    await message.answer("В Краснодаре сейчас температура: " + str(temp_temperature) + " по Цельсию.")

@dp.message_handler(Text(equals="🌧Осадки🌧"))
async def rainfall(message: types.Message):
    await message.answer("Осадки в Краснодаре " + w.detailed_status)




executor.start_polling(dp, skip_updates=True,on_startup=on_startup)





