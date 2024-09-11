from core.database.models import async_session
from core.database.models import Expense, Income
from sqlalchemy import select, func
from datetime import datetime


async def new_income(income: dict, tg_id: str, date: datetime):
    async with async_session() as session:
        session.add(Income(tg_id=tg_id, amount=income['amount'], date=date.date()))
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