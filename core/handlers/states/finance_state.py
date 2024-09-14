from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from re import fullmatch
from asyncio import to_thread

from core.database import requests as rq


class Finance(StatesGroup):

    period_of_time = State()


router = Router()

@router.message(Command('finance'))
async def finance_period(message: Message, state: FSMContext):
    await state.set_state(Finance.period_of_time)
    await message.answer('укажите за какой период отобразить сводку доходов и расходов в формате:\n\n'
                         '1D т.е. 1 день\n3M - 3 месяца\n1Y - 1 год\n'
                         'ввести можно лишь одно значение\n\n'
                         'или напишите all чтобы получить сводку за все время')

@router.message(Finance.period_of_time)
async def display_finance(message: Message, state: FSMContext):
    period = message.text
    if fullmatch(r'^\d+[DMY]$', period) or period == 'all':
        if period == 'all':
            income, expense = await rq.get_finance_all(message.from_user.id)
        else:
            income, expense = await rq.get_finance(message.from_user.id, period)
        all_income = await to_thread(amount_of_money, income)
        all_expense = await to_thread(amount_of_money, expense)
        categories = await to_thread(top_category, expense)
        message_categories = ''
        if len(categories) >= 1:
            message_categories = 'топ категорий по трате:\n\n'f'{''.join(f'{category} - {amount} руб.\n' 
                                                                         for category, amount in categories.items())}'
        await message.answer('ваша статистика за данный период:\n\n'
                            f'заработано: {all_income} руб.\n'
                            f'потрачено: {all_expense} руб.\n\n'
                            + message_categories)
        await state.clear()
        return

    await message.answer('введите период в правильном формате')

def amount_of_money(finance):
    all_money = 0

    for el in finance:
        all_money += el.amount

    return all_money

def top_category(expenses):
    category = {}

    for expense in expenses:
        cat = expense.category
        if category.get(cat) is not None:
            continue
        all_money = 0
        for el in expenses:
            if el.category == cat:
                all_money += el.amount
        category[cat] = all_money
    
    sorted_categories = dict(sorted(category.items(), key=lambda item: item[1], reverse=True)[:4])

    return sorted_categories 