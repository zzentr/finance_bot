from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from core.database import requests as rq


async def categories(tg_id: str):
    keyboard = ReplyKeyboardBuilder()
    all_categories = await rq.get_categories(tg_id)

    for cat in all_categories:
        keyboard.add(KeyboardButton(text=cat))

    return keyboard.adjust(2).as_markup(resize_keyboard=True)