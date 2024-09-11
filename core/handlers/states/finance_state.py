from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


class Finance(StatesGroup):

    period_of_time = State()


router = Router()

@router.message(Command('finance'))
async def finance_period(message: Message, state: FSMContext):
    await state.set_state(Finance.period_of_time)
    await message.answer('укажите за какой период отобразить сводку доходов и расходов.\n'
                         'формат: 1D; M; 1Y где D-день, M-месяц, Y-год.\n например 1M - 1 месяц')

@router.message(Finance.period_of_time)
async def display_finance(message: Message, state: FSMContext):
    period = message.text