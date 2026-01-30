import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiohttp import web

# 1. ПЕРЕМЕННЫЕ
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
if ADMIN_ID:
    ADMIN_ID = int(ADMIN_ID)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 2. КЛАВИАТУРА
kb = [
    [KeyboardButton(text="Мои услуги"), KeyboardButton(text="Цены")],
    [KeyboardButton(text="Портфолио")],
    [KeyboardButton(text="Оставить заявку")]
]
menu = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# 3. МИНИ-СЕРВЕР ДЛЯ RENDER
async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get("/", handle)

# 4. ОБРАБОТЧИКИ (ХЕНДЛЕРЫ)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}! Выберите действие в меню:", reply_markup=menu)

@dp.message(lambda message: message.text == "Цены")
async def price_handler(message: types.Message):
    await message.answer("💰 Мой прайс:\n- Бот-визитка: 3000 сом\n- Сложный бот: от 7000 сом")

@dp.message(lambda message: message.text == "Портфолио")
async def portfolio_handler(message: types.Message):
    # Если файла work.png нет на сервере, бот выдаст ошибку, поэтому используем try
    try:
        photo = FSInputFile("work.png")
        await message.answer_photo(photo, caption="🚀 Мои работы")
    except:
        await message.answer("🚀 Портфолио: здесь будут мои работы.")

@dp.message(lambda message: message.text == "Мои услуги")
async def services_handler(message: types.Message):
    await message.answer("🛠 Я создаю Telegram ботов на Python для автоматизации вашего бизнеса.")

@dp.message(lambda message: message.text == "Оставить заявку")
async def order_handler(message: types.Message):
    await message.answer("🤝 Напишите ваш номер телефона или @username, и я свяжусь с вами!")

# Сбор контактов (если в сообщении есть цифры)
# Обработка заявок (замени этот хендлер в своем коде)
@dp.message()
async def handle_all_messages(message: types.Message):
    # Проверяем, есть ли в сообщении цифры (похоже на номер телефона)
    if any(char.isdigit() for char in message.text):
        await message.answer("✅ Спасибо! Заявка отправлена. Скоро свяжусь.")
        
        if ADMIN_ID:
            user = message.from_user
            # Формируем ссылку на пользователя
            if user.username:
                user_link = f"@{user.username}"
            else:
                user_link = "Ник не установлен"
            
            # Собираем полную информацию
            info = (
                f"🌟 **НОВАЯ ЗАЯВКА!**\n\n"
                f"👤 **Имя:** {user.full_name}\n"
                f"🔗 **Юзернейм:** {user_link}\n"
                f"🆔 **ID:** `{user.id}`\n"
                f"📱 **Сообщение/Номер:** {message.text}"
            )
            
            # Отправляем админу (тебе)
            await bot.send_message(ADMIN_ID, info, parse_mode="Markdown")
    else:
        await message.answer("Пожалуйста, используйте кнопки меню или оставьте номер телефона для связи.")

# 5. ЗАПУСК
async def main():
    # Запуск веб-сервера на порту Render
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    # Очистка старых сообщений и старт бота
    await bot.delete_webhook(drop_pending_updates=True)
    print(f"Бот запущен на порту {port}...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())




