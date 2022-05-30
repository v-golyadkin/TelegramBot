from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import types

client_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
remove_keyboard = types.ReplyKeyboardRemove()
buttons_command=['🌡Погода🌡','🌧Осадки🌧']
buttons_command_=['💧Влажность💧','💨Скорость ветра💨']

button_edit=['Изменить город']
button_exit=['Закрыть меню']
client_keyboard.add(*buttons_command).add(*buttons_command_).row(*button_edit).row(*button_exit)
