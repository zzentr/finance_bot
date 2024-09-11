from aiogram import F, Router
from aiogram.types import Message


router = Router()


@router.message()
async def other(message: Message):
    await message.answer('для работы со мной отправьте мне команду!')