@echo off

call %~dp0TelegramBot\venv\Scripts\activate

cd %~dp0TelegramBot

set TOKEN=###################################

python telegram_bot.py

pause
