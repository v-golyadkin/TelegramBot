from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,  ReplyKeyboardRemove


weather = KeyboardButton('Погода')
rainfall = KeyboardButton('Осадки')


keyboard = ReplyKeyboardMarkup()

keyboard.add(weather).add(rainfall)