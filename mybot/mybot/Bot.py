import asyncio
import logging
import random
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Нужен для корректной работы на некоторых серверах
nest_asyncio.apply()

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен бота
BOT_TOKEN = "ТВОЙ_ТОКЕН"
# ID канала
CHANNEL_ID = "@ТВОЙ_КАНАЛ"

# Источники новостей
sources = {
    "UNCTAD": "https://unctad.org/",
    "Open Innovations": "https://openinnovations.ru/",
    "WIPO": "https://www.wipo.int/",
    "Stat.uz": "https://stat.uz/"
}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Новости UNCTAD", callback_data="UNCTAD")],
        [InlineKeyboardButton("Новости Open Innovations", callback_data="Open Innovations")],
        [InlineKeyboardButton("Новости WIPO", callback_data="WIPO")],
        [InlineKeyboardButton("Новости Stat.uz", callback_data="Stat.uz")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать! Выберите источник новостей:",
        reply_markup=reply_markup
    )

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    source = query.data
    url = sources.get(source)

    photo_url = "https://source.unsplash.com/800x600/?" + random.choice(["finance", "technology", "innovation", "news"])

    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=photo_url,
        caption=f"Новости из {source}:\n{url}"
    )
    await query.edit_message_text(text=f"Отправил новости {source} в канал!")

# Автоматическая отправка новостей
async def post_random_news(bot):
    source_name, url = random.choice(list(sources.items()))
    photo_url = "https://source.unsplash.com/800x600/?" + random.choice(["finance", "technology", "innovation", "news"])

    await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=photo_url,
        caption=f"Новости из {source_name}:\n{url}"
    )

# Основная функция
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Планировщик отправки
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(post_random_news(application.bot)), 'cron', hour=10)
    scheduler.add_job(lambda: asyncio.create_task(post_random_news(application.bot)), 'cron', hour=12)
    scheduler.add_job(lambda: asyncio.create_task(post_random_news(application.bot)), 'cron', hour=14)
    scheduler.add_job(lambda: asyncio.create_task(post_random_news(application.bot)), 'cron', hour=16)
    scheduler.start()

    print("Бот запущен!")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
