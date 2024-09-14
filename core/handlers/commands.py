from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('добро пожаловать, я помогу вам управлять финансами, следить за доходами и расходами')

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('я бот для управления вашими финансами, используйте команды ниже\n\n'
                         '/add_income - добавить доход\n'
                         '/add_expense - добавить расход')

