import requests
from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from keyboards import weather_keyboard

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n")
    await message.answer(
        f"Напиши мне любой город России и я отправлю тебе его погоду!", reply_markup=weather_keyboard()
    )


@router.message()
async def weather_handler(message: types.Message) -> None:
    if message.text == 'Узнать погоду':
        await message.answer(
            f"Напиши мне любой город России и я отправлю тебе его погоду!", reply_markup=weather_keyboard()
        )
        return

    try:
        response = requests.get(
            f"http://backend:8000/api/weather?city={message.text}&username={message.from_user.full_name}"
        )
        await message.answer(
            response.text.replace("\"", '').replace('\\n', '\n'),
            reply_markup=weather_keyboard(),
            parse_mode=ParseMode.HTML
        )
    except TypeError:
        await message.answer("Непредвиденная ошибка!")
