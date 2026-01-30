import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web # Добавили эту библиотеку

# 1. ПЕРЕМЕННЫЕ
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
if ADMIN_ID:
    ADMIN_ID = int(ADMIN_ID)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ХИТРОСТЬ ДЛЯ БЕСПЛАТНОГО ТАРИФА ---
# Создаем простой веб-сервер, чтобы Render не убивал процесс
async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get("/", handle)
# ---------------------------------------

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Привет! Бот работает бесплатно на Render.")

# Основная функция запуска
async def main():
    # Запускаем веб-сервер на порту, который даст Render
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


