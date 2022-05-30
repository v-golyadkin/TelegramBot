from email import message
from lib2to3.pgen2.token import EQUAL
from aiogram import Dispatcher, types
from create_bot import dp, bot

from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from keyboards import client_keyboard,remove_keyboard
import pyowm

from pyowm.utils.config import get_default_config

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db import DataBase

db = DataBase("database.db")

class FSMPlace(StatesGroup):
    place=State()
    editplace=State()


config_dict = get_default_config()
config_dict['language'] = 'ru' 

owm = pyowm.OWM('778da4a75335bc96792e7075b5831234', config_dict)
mgr = owm.weather_manager()

async def command_start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await FSMPlace.place.set()
        await message.answer("Введите город")
    else:
        await message.answer("Выберите что хотите узнать",reply_markup=client_keyboard)


async def command_set_place(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['place'] = message.text
        db.set_city(message.from_user.id,message.text)
        await state.finish()
        await message.answer("Выберите что хотите узнать",reply_markup=client_keyboard)
       
async def command_edit(message: types.message):
    await message.answer("Введите ваш город",reply_markup=remove_keyboard)
    await FSMPlace.editplace.set()

    
async def command_final_edit(message: types.message,state:FSMContext):
    async with state.proxy() as data:
        data['editplace'] = message.text
        db.set_city(message.from_user.id,message.text)
        await state.finish()
        await message.answer("Выберите что хотите узнать",reply_markup=client_keyboard)

async def command_weather(message: types.Message):
    city=str(db.get_user_place(message.from_user.id)[0][0])
    observation = mgr.weather_at_place(city)
    w = observation.weather
    temp_temperature = int(w.temperature('celsius')['temp'])
    feels_like_temperature = int(w.temperature('celsius')['feels_like'])
    await message.answer("Сейчас в городе " + city + " температура " + str(temp_temperature) +"°C, ощущается как "+ str(feels_like_temperature)+"°C")

async def command_rainfall(message: types.Message):
    city=str(db.get_user_place(message.from_user.id)[0][0])
    observation = mgr.weather_at_place(city)
    w = observation.weather
    await message.answer("В городе " + city + " сейчас " + w.detailed_status)

async def command_humidity(message: types.Message):
    city=str(db.get_user_place(message.from_user.id)[0][0])
    observation = mgr.weather_at_place(city)
    w = observation.weather
    await message.answer("В городе " + city + " влажность сейчас " + str(w.humidity) + "%")

async def command_wind(message: types.Message):
    city=str(db.get_user_place(message.from_user.id)[0][0])
    observation = mgr.weather_at_place(city)
    w = observation.weather
    wind_=w.wind()['speed']
    await message.answer("В городе " + city + " скорость ветра " + str(wind_) + "м/c")

async def command_menu(message: types.Message):
    await message.answer("Выберите что хотите узнать",reply_markup=client_keyboard)

async def command_clear_keyboard(message: types.Message):
    await message.answer("Клавиатура была убрана",reply_markup=remove_keyboard)

async def command_ignore(message: types.Message):
        if db.get_user_activity(message.from_user.id)[0][0] == 1:
            db.set_activity(message.from_user.id,0)
            await message.answer("Рассылка была выключена")
        else:
            db.set_activity(message.from_user.id,1)
            await message.answer("Рассылка была включена")

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start','help'], state=None)
    dp.register_message_handler(command_set_place, state = FSMPlace.place)
    dp.register_message_handler(command_edit, Text(equals="Изменить город"))
    dp.register_message_handler(command_final_edit,state = FSMPlace.editplace)
    dp.register_message_handler(command_menu, commands=['menu'], state=None)
    
    dp.register_message_handler(command_edit, commands=['edit'])
    dp.register_message_handler(command_weather, commands=['weather'])
    dp.register_message_handler(command_rainfall, commands=['rainfall'])
    dp.register_message_handler(command_humidity, commands=['humidity'])
    dp.register_message_handler(command_wind, commands=['wind'])
    dp.register_message_handler(command_ignore, commands=['ignore'])

    dp.register_message_handler(command_weather, Text(equals="🌡Погода🌡"))
    dp.register_message_handler(command_rainfall, Text(equals="🌧Осадки🌧"))
    dp.register_message_handler(command_humidity, Text(equals="💧Влажность💧"))
    dp.register_message_handler(command_wind, Text(equals="💨Скорость ветра💨"))
    dp.register_message_handler(command_clear_keyboard, Text(equals="Закрыть меню"))