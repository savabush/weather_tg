from aiogram import types


def weather_keyboard():
    kb = [
        [types.KeyboardButton(text="Узнать погоду")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder='Напишите город')
    return keyboard
