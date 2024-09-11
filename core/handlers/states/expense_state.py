from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from re import fullmatch

from core.database import requests as rq
from core.keyboards import reply 


router = Router()


class Expense(StatesGroup):
    
    amount = State()
    category = State()


@router.message(Command('add_expense'))
async def cmd_expense(message: Message, state: FSMContext):
    await state.set_state(Expense.amount)
    await message.answer('введите сумму вашего расхода')

@router.message(Expense.amount)
async def amount_expense(message: Message, state: FSMContext):
    amount = message.text
    try:
        amount = float(amount)
    except ValueError:
        await message.answer('введите числовое значение расхода в RUB')
        return
    if amount <= 0:
        await message.answer('введите число больше нуля')
        return
    await state.update_data(amount=amount)
    await state.set_state(Expense.category)
    await message.answer('выберите категорию расхода', reply_markup=await reply.categories(message.from_user.id))

@router.message(Expense.category)
async def category_expense(message: Message, state: FSMContext):
    category = message.text.strip()
    if not fullmatch(r'[A-Za-zА-Яа-яЁё]+', category):
        await message.answer('введите категорию состоящую только из букв')
        return
    await state.update_data(category=category)
    data = await state.get_data()
    await rq.new_expense(data, message.from_user.id, message.date)
    await message.answer('спасибо, я сохранил ваши ответы!', reply_markup=ReplyKeyboardRemove())
    await state.clear()


