from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from core.database import requests as rq


router = Router()


class Income(StatesGroup):
    
    amount = State()


@router.message(Command('add_income'))
async def cmd_income(message: Message, state: FSMContext):
    await state.set_state(Income.amount)
    await message.answer('введите сумму вашего дохода в RUB')

@router.message(Income.amount)
async def amount_income(message: Message, state: FSMContext):
    amount = message.text
    try:
        amount = float(amount)
    except ValueError:
        await message.answer('введите числовое значение дохода')
        return
    if amount <= 0:
        await message.answer('введите число больше нуля')
        return
    await rq.new_income(amount, message.from_user.id, message.date)
    await message.answer('спасибо, я сохранил ваш ответ!')
    await state.clear()


