from core.database.models import async_session
from core.database.models import Expense, Income
from sqlalchemy import select, func
from datetime import datetime, timedelta
from asyncio import to_thread


async def new_income(income: str, tg_id: str, date: datetime):
    async with async_session() as session:
        session.add(Income(tg_id=tg_id, amount=int(income), date=date.date()))
        await session.commit()

async def new_expense(expense: dict, tg_id: str, date: datetime):
    async with async_session() as session:
        session.add(Expense(tg_id=tg_id, amount=expense['amount'], date=date.date(), category=expense['category'].lower()))
        await session.commit()
    
async def get_categories(tg_id: str):
    async with async_session() as session:
        categories = await session.scalars(select(Expense.category)
                                           .where(Expense.tg_id == tg_id)
                                           .group_by(Expense.category)
                                           .order_by(func.count(Expense.category)
                                            .desc()).limit(4))
        await session.commit()
        return categories
    
async def get_finance(tg_id: str, period: str):
    async with async_session() as session:
        period_date = await to_thread(calculate_days, period)

        income_query = select(Income).where(Income.date >= period_date.date(), Income.tg_id == tg_id)
        expense_query = select(Expense).where(Expense.date >= period_date.date(), Expense.tg_id == tg_id)

        income = await session.scalars(income_query)
        expense = await session.scalars(expense_query)

        return income.all(), expense.all()

def calculate_days(period: str):
    days_dict = {'D': 1, 'M': 30, 'Y': 365}
    days = int(period[0]) * days_dict[period[1]]
    return datetime.now() - timedelta(days=days)

async def get_finance_all(tg_id: str):
    async with async_session() as session:

        income_query = select(Income).where(Income.tg_id == tg_id)
        expense_query = select(Expense).where(Expense.tg_id == tg_id)

        income = await session.scalars(income_query)
        expense = await session.scalars(expense_query)
        
        return income.all(), expense.all()