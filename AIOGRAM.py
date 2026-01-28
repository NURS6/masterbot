import asyncio
import re
import os
from aiogram import Bot, Dispatcher, types 
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

# Вставь сюда токен, который тебе дал @BotFather
#ОТПРАВЛЯЕМ ЛИД ТЕБЕ

    admin_id = os.getenv('ADMIN_ID')
    if admin_id:
        await bot.send_message(admin_id, f"🔥 НОВЫЙ ЛИД!\nИмя: {user_name}\nTG: {username}")

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

kb = [
    [KeyboardButton(text="Мои услуги"), KeyboardButton(text="Цены")],
    [KeyboardButton(text="Портфолио")],
    [KeyboardButton(text="Оставить заявку")]
]
menu = ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer (f"{user_name} Выбери действие в меню:", reply_markup=menu)

    # Ответ на кнопку "Цены"
@dp.message(lambda message: message.text == "Цены")
async def price_handler(message: types.Message):
    await message.answer("💳 Мой прайс:\n- Бот-визитка: 3000 сом\n- Сложный бот: от 7000 сом")

#  кнопка "Портфолио"
@dp.message(lambda message: message.text == "Портфолио")
async def portfolio_handler(message: types.Message):
    # 1. Создаем объект фото из файла в твоей папке
    photo = FSInputFile("work.png")
    
    # 2. Отправляем именно ФОТО, а не просто текст
    await message.answer_photo(
        photo=photo, 
        caption="🚀 <b>Мои работы:</b>\nЯ создаю надежных ботов для бизнеса🤖.",
        parse_mode="HTML"
    )
# Ответ на кнопку "Мои услуги"
@dp.message(lambda message: message.text == "Мои услуги")
async def services_handler(message: types.Message):
    await message.answer("🛠 Я создаю Telegram ботов на Python для автоматизации вашего бизнеса.")

# Ответ на кнопку "Оставить заявку"
@dp.message(lambda message: message.text == "Оставить заявку")
async def order_handler(message: types.Message):
    # Берем имя пользователя, чтобы ответ был персональным
    user_name = message.from_user.first_name
    await message.answer(
        f"🤝 {user_name}, я готов обсудить ваш проект!\n\n"
        "Пожалуйста, напишите ваш номер телефона или @username для связи. "
        "Также можете кратко описать, какой бот вам нужен. Я отвечу в течение часа."
    )


@dp.message()
async def handle_all_messages(message: types.Message):
    # Проверяем, есть ли в сообщении цифры (похоже ли это на номер)
    if any(char.isdigit() for char in message.text):
        # 1. Отвечаем клиенту
        await message.answer("✅ Принято! Я передал ваши данные мастеру. Ожидайте связи.")
        
        # 2. Уведомление
        user = message.from_user
        info = (
            f"🚀 НОВАЯ ЗАЯВКА (Номер телефона)!\n\n"
            f"👤 Клиент: {user.full_name}\n"
            f"🔗 Ссылка: @{user.username if user.username else 'скрыт'}\n"
            f"📱 Контакт: {message.text}"
        )
        await bot.send_message(chat_id=ADMIN_ID, text=info)
    else:
        # Если это просто текст без цифр
        await message.answer("Чтобы оставить заявку, пожалуйста, напишите ваш номер телефона.")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':

    asyncio.run(main())
