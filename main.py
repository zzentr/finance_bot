from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from asyncio import run
import os
load_dotenv()

from core.handlers import text, commands, callbacks
from core.handlers.states import expense_state, income_state, finance_state
from core.database.models import async_main


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    dp.include_routers(commands.router, callbacks.router, 
                       expense_state.router, income_state.router, finance_state.router, 
                       text.router)
    await async_main()
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())