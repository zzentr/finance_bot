from sqlalchemy import BigInteger, Integer, Float, Date, String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os
load_dotenv()


engine = create_async_engine(url=os.getenv('BD_URL'))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Expense(Base):
    __tablename__ = 'expenses'

    id = mapped_column(Integer, primary_key=True)
    tg_id = mapped_column(BigInteger)
    amount = mapped_column(Float)
    date = mapped_column(Date)
    category = mapped_column(String)


class Income(Base):
    __tablename__ = 'incomes'

    id = mapped_column(Integer, primary_key=True)
    tg_id = mapped_column(BigInteger)
    amount = mapped_column(Float)
    date = mapped_column(Date)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


