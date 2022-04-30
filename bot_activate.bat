@echo off

call %~dp0TelegramBot\venv\Scripts\activate

cd %~dp0TelegramBot

set TOKEN=5116472695:AAGsZlKDdLmLgolpQARsXCOrXyLKOhHz6cM

python telegram_bot.py

pause