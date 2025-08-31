from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from asyncio import run, create_task
import os
load_dotenv()

from core.handlers import text, commands
from core.handlers.states import expense_state, income_state, finance_state
from core.database.models import async_main


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

async def handle(request):
    return web.Response(text="Bot is running ✅")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    dp.include_routers(commands.router,
                       expense_state.router, income_state.router, finance_state.router, 
                       text.router)
    await async_main()
    create_task(start_web_server())
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
