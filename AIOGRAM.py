import asyncio
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import CommandStart

# --- 1. ИНИЦИАЛИЗАЦИЯ (Заменяем строки 9-17) ---
TOKEN = os.getenv('BOT_TOKEN')
# Преобразуем в число сразу, чтобы не было ошибок при отправке
ADMIN_ID = os.getenv('ADMIN_ID')
if ADMIN_ID:
    ADMIN_ID = int(ADMIN_ID)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 2. КЛАВИАТУРА ---
kb = [
    [KeyboardButton(text="Мои услуги"), KeyboardButton(text="Цены")],
    [KeyboardButton(text="Портфолио")],
    [KeyboardButton(text="Оставить заявку")]
]
menu = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- 3. ОБРАБОТЧИКИ (ХЕНДЛЕРЫ) ---

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f"{user_name}, выберите действие в меню:", reply_markup=menu)

@dp.message(lambda message: message.text == "Цены")
async def price_handler(message: types.Message):
    await message.answer("💰 Мой прайс:\n- Бот-визитка: 3000 сом\n- Сложный бот: от 7000 сом")

@dp.message(lambda message: message.text == "Портфолио")
async def portfolio_handler(message: types.Message):
    photo = FSInputFile("work.png")
    await message.answer_photo(
        photo=photo,
        caption="🚀 <b>Мои работы:</b>\nЯ создаю надежных ботов для бизнеса 🤖",
        parse_mode="HTML"
    )

@dp.message(lambda message: message.text == "Мои услуги")
async def services_handler(message: types.Message):
    await message.answer("🛠 Я создаю Telegram ботов на Python для автоматизации вашего бизнеса.")

@dp.message(lambda message: message.text == "Оставить заявку")
async def order_handler(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"🤝 {user_name}, я готов обсудить ваш проект!\n\n"
        "Пожалуйста, напишите ваш номер телефона или @username для связи. "
        "Также можете кратко описать, какой бот вам нужен."
    )

# Обработка всех остальных сообщений (сбор заявок)
@dp.message()
async def handle_all_messages(message: types.Message):
    # Проверяем, есть ли в сообщении цифры (похоже на номер)
    if any(char.isdigit() for char in message.text):
        await message.answer("✅ Принято! Я передал ваши данные мастеру. Ожидайте связи.")
        
        # УВЕДОМЛЕНИЕ АДМИНУ (Исправлено)
        if ADMIN_ID:
            user = message.from_user
            info = (
                f"🌟 НОВАЯ ЗАЯВКА!\n\n"
                f"👤 Клиент: {user.full_name}\n"
                f"🔗 Ссылка: @{user.username if user.username else 'скрыта'}\n"
                f"📱 Контакт/Текст: {message.text}"
            )
            await bot.send_message(chat_id=ADMIN_ID, text=info)
    else:
        await message.answer("Чтобы оставить заявку, пожалуйста, напишите ваш номер телефона.")

# --- 4. ЗАПУСК (Заменяем строки 86-91) ---
async def main():
    # Уведомление в консоль и админу при старте
    print("Бот запущен...")
    if ADMIN_ID:
        try:
            await bot.send_message(chat_id=ADMIN_ID, text="🚀 Бот успешно запущен на Render!")
        except Exception as e:
            print(f"Ошибка уведомления админа: {e}")

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


