from aiogram import Dispatcher, types
from create_bot import dp, bot
from db import DataBase


db = DataBase("database.db")




async def command_sendall(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == 466463411:
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if row[1] != 1: 
                        db.set_activity(row[0],1)
                except:
                    db.set_activity(row[0],0)
            await bot.send_message(message.from_user.id,"Рассылка прошла успешно")

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(command_sendall, commands=['sendall'])