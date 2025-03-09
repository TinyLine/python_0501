import asyncio
import random
import aiohttp
import feedparser
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import re
from html import unescape
from deep_translator import GoogleTranslator

TOKEN = "7838252070:AAHjgGtCy9DofzM94u7OlpLnPd4wTFykJ3U"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ========================== КНОПКИ МЕНЮ ========================== #
keyboard = ReplyKeyboardMarkup(
    keyboard=[  
        [KeyboardButton(text="ℹ️ Про бота"),
         KeyboardButton(text="🪙 Кинути монетку"),
         KeyboardButton(text="🎮 Знижки Steam"),
         KeyboardButton(text="📰 Новини ігор")],
    ],
    resize_keyboard=True
)

# Клавиатура для кнопки "Більше новин" и "Вийти"
more_news_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📰 Більше новин")],
        [KeyboardButton(text="❌ Вийти з новин")],
    ],
    resize_keyboard=True
)

# Переменная для отслеживания позиции новостей
news_state = {}



# ========================== ОБРОБКА КОМАНД ========================== #
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привіт! Я твій Telegram-бот! 🚀", reply_markup=keyboard)

@dp.message(Command("about"))
@dp.message(lambda message: message.text == "ℹ️ Про бота")
async def about_message(message: Message):
    await message.answer("🤖 Привіт! Я твій помічник у світі ігор та розваг.")

@dp.message(Command("flip"))
@dp.message(lambda message: message.text == "🪙 Кинути монетку")
async def flip_command(message: Message):
    result = random.choice(['Орёл', 'Решка'])
    await message.answer(f"🪙 Результат підкидання монети: {result}")

@dp.message(Command("sales"))
@dp.message(lambda message: message.text == "🎮 Знижки Steam")
async def steam_sales_command(message: Message):
    games = await get_steam_discounts()

    if not games:
        await message.answer("❌ Зараз немає ігор зі знижкою 20%+.")  
        return

    for game in games[:10]:  # Вивести максимум 10 ігор
        text = (
            f"🎮 *{game['name']}* - Супер пропозиція!\n"
            f"💰 *Знижка*: ~{game['original_price']} UAH~ → *{game['discounted_price']} UAH* (-{game['discount']}%)\n"
            f"💵 *Ціна в доларах*: ~{game['original_price_usd']}$~ → *{game['discounted_price_usd']}$*\n"
            f"🔗 [Купити гру]({game['url']})"
        )
        
        await message.answer_photo(photo=game["image"], caption=text, parse_mode="Markdown")

@dp.message(Command("news"))
@dp.message(lambda message: message.text == "📰 Новини ігор")
async def game_news_command(message: Message):
    news_list = await get_game_news()

    if not news_list:
        await message.answer("❌ На жаль, немає новин для показу.")
        return

    # Сохраняем состояние, если это первый запрос
    user_id = message.from_user.id
    if user_id not in news_state:
        news_state[user_id] = {'index': 0, 'news_list': news_list}

    # Показываем первые 3 новости
    start_index = news_state[user_id]['index']
    end_index = start_index + 3
    for news in news_list[start_index:end_index]:
        clean_summary = remove_html_tags(news['summary'])
        translated_summary = await translate_to_ukrainian(clean_summary)  # Переводим описание
        await message.answer(
            f"📰 {news['title']}\n"
            f"📅 {news['published']}\n"
            f"{translated_summary}\n"  # Переведенный короткий опис
            f"🔗 [Читати більше]({news['link']})"
        )

    # Обновляем индекс для следующего запроса
    news_state[user_id]['index'] = end_index

    # Добавляем кнопку для получения больше новостей
    if end_index < len(news_list):
        await message.answer("Щоб побачити більше новин, натискайте кнопку нижче:", reply_markup=more_news_keyboard)
    else:
        await message.answer("Це всі новини на цей момент.")

@dp.message(lambda message: message.text == "📰 Більше новин")
async def more_news_command(message: Message):
    user_id = message.from_user.id
    if user_id not in news_state:
        await message.answer("❌ Немає доступних новин.")
        return

    news_list = news_state[user_id]['news_list']
    start_index = news_state[user_id]['index']
    end_index = start_index + 3

    if start_index < len(news_list):
        for news in news_list[start_index:end_index]:
            clean_summary = remove_html_tags(news['summary'])
            translated_summary = await translate_to_ukrainian(clean_summary)  # Переводим описание
            await message.answer(
                f"📰 {news['title']}\n"
                f"📅 {news['published']}\n"
                f"{translated_summary}\n"
                f"🔗 [Читати більше]({news['link']})"
            )

        news_state[user_id]['index'] = end_index  # Обновляем индекс

        if end_index < len(news_list):
            await message.answer("Щоб побачити більше новин, натискайте кнопку нижче:", reply_markup=more_news_keyboard)
        else:
            await message.answer("Це всі новини на цей момент.")
    else:
        await message.answer("❌ Немає доступних новин.")

@dp.message(lambda message: message.text == "❌ Вийти з новин")
async def exit_news_command(message: Message):
    await message.answer("Ви вийшли з розділу новин.", reply_markup=keyboard)
    # Очищаем состояние новостей
    user_id = message.from_user.id
    if user_id in news_state:
        del news_state[user_id]

# ========================== УДАЛЕНИЕ HTML ТЕГОВ ========================== #
def remove_html_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    clean_text = unescape(clean_text)
    return clean_text

# ========================== ПЕРЕВОД НА УКРАИНСКИЙ ========================== #
async def translate_to_ukrainian(text):
    translated = GoogleTranslator(source='auto', target='uk').translate(text)
    return translated

# ========================== ФУНКЦІЯ ДЛЯ ОТРИМАННЯ НОВИН ========================== #
async def get_game_news():
    RSS_FEED = "https://www.rockpapershotgun.com/feed"
    feed = feedparser.parse(RSS_FEED)

    news_list = []

    for entry in feed.entries[:10]:  # Получаем первые 10 новостей
        news_item = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary
        }
        news_list.append(news_item)

    return news_list

# ========================== STEAM API ========================== #
async def get_steam_discounts():
    STEAM_API_URL = "https://store.steampowered.com/api/featuredcategories/?cc=UA&l=uk"
    USD_EXCHANGE_RATE = 40

    async with aiohttp.ClientSession() as session:
        async with session.get(STEAM_API_URL) as response:
            if response.status != 200:
                print("❌ Помилка запиту до Steam API")
                return []

            data = await response.json()

            if "specials" not in data or "items" not in data["specials"]:
                print("❌ Немає ігор зі знижками")
                return []

            games = []
            seen_ids = set()

            for game in data["specials"]["items"]:
                game_id = game.get("id")
                discount = game.get("discount_percent", 0)
                original_price = game.get("original_price", 0) / 100
                discounted_price = game.get("final_price", 0) / 100

                if discount < 20 or game_id in seen_ids:
                    continue  

                games.append({
                    "name": game.get("name"),
                    "original_price": f"{original_price:.2f}",
                    "discounted_price": f"{discounted_price:.2f}",
                    "original_price_usd": f"{original_price / USD_EXCHANGE_RATE:.2f}",
                    "discounted_price_usd": f"{discounted_price / USD_EXCHANGE_RATE:.2f}",
                    "discount": discount,
                    "url": f"https://store.steampowered.com/app/{game_id}/",
                    "image": f"https://cdn.akamai.steamstatic.com/steam/apps/{game_id}/header.jpg"
                })
                seen_ids.add(game_id)

            return games

# ========================== ЗАПУСК БОТА ========================== #
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
