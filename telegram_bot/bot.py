import asyncio
import random
import aiohttp
import feedparser
import re
from html import unescape
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from deep_translator import GoogleTranslator


TOKEN = "7838252070:AAHjgGtCy9DofzM94u7OlpLnPd4wTFykJ3U"

bot = Bot(token=TOKEN)
dp = Dispatcher()
news_state = {}
USD_EXCHANGE_RATE = 40
STEAM_API_URL = "https://store.steampowered.com/api/featuredcategories/?cc=UA&l=uk"
RSS_FEED = "https://www.rockpapershotgun.com/feed"



# ========================== КНОПКИ МЕНЮ ========================== #
keyboard = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="ℹ️ Про бота"),
        KeyboardButton(text="🪙 Кинути монетку"),
        KeyboardButton(text="🎮 Знижки Steam"),
        KeyboardButton(text="📰 Новини ігор")
    ]], resize_keyboard=True
)
more_news_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📰 Більше новин")],
        [KeyboardButton(text="❌ Вийти з новин")]
    ], resize_keyboard=True
)



# ========================== ОБРОБКА КОМАНД ========================== #
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привіт! Я твій Telegram-бот! 🚀", reply_markup=keyboard)

@dp.message(lambda message: message.text == "ℹ️ Про бота")
async def about_command(message: Message):
    await message.answer("🤖 Привіт! Я твій помічник у світі ігор та розваг.")

@dp.message(lambda message: message.text == "🪙 Кинути монетку")
async def flip_command(message: Message):
    await message.answer(f"🪙 Результат: {random.choice(['Орёл', 'Решка'])}")

@dp.message(lambda message: message.text == "🎮 Знижки Steam")
async def steam_sales_command(message: Message):
    games = await get_steam_discounts()
    if not games:
        await message.answer("❌ Немає ігор зі знижкою 20%+.")
        return
    for game in games[:10]:
        await message.answer_photo(
            photo=game["image"],
            caption=(
                f"🎮 *{game['name']}*\n💰 *Знижка*: ~{game['original_price']} UAH~ → *{game['discounted_price']} UAH* (-{game['discount']}%)\n"
                f"💵 *Ціна в доларах*: ~{game['original_price_usd']}$~ → *{game['discounted_price_usd']}$*\n🔗 [Купити гру]({game['url']})"
            ), parse_mode="Markdown"
        )

@dp.message(lambda message: message.text in ["📰 Новини ігор", "📰 Більше новин"])


async def game_news_command(message: Message):
    user_id = message.from_user.id
    
    if message.text == "📰 Новини ігор":
        news_list = await get_game_news()
        
        if not news_list:
            await message.answer("❌ На жаль, немає новин для показу.")
            return
        news_state[user_id] = {'index': 0, 'news_list': news_list}
        
    else:
        
        if user_id not in news_state:
            await message.answer("❌ Немає доступних новин.")
            return
    
    news_list, start_index = news_state[user_id]['news_list'], news_state[user_id]['index']
    end_index = start_index + 3
    
    for news in news_list[start_index:end_index]:
        await message.answer(
            f"📰 {news['title']}\n📅 {news['published']}\n{await translate_to_ukrainian(remove_html_tags(news['summary']))}\n🔗 [Читати більше]({news['link']})"
        )
    news_state[user_id]['index'] = end_index

    if end_index < len(news_list):
        await message.answer("Щоб побачити більше новин, натискайте кнопку нижче:", reply_markup=more_news_keyboard)
    else:
        await message.answer("Це всі новини на цей момент.")


@dp.message(lambda message: message.text == "❌ Вийти з новин")
async def exit_news_command(message: Message):
    
    user_id = message.from_user.id
    news_state.pop(user_id, None)
    await message.answer("Ви вийшли з розділу новин.", reply_markup=keyboard)



# ========================== УТИЛИТАРНІ ФУНКЦІЇ ========================== #
def remove_html_tags(text):
    return unescape(re.sub(r'<.*?>', '', text))

async def translate_to_ukrainian(text):
    return GoogleTranslator(source='auto', target='uk').translate(text)

async def get_game_news():
    feed = feedparser.parse(RSS_FEED)
    return [
        {"title": entry.title, "link": entry.link, "published": entry.published, "summary": entry.summary}
        for entry in feed.entries[:10]
    ]


async def get_steam_discounts():
    async with aiohttp.ClientSession() as session:
        async with session.get(STEAM_API_URL) as response:    
            if response.status != 200:
                return []
            data = await response.json()
            
            return [
                {
                    "name": game["name"],
                    "original_price": f"{game["original_price"] / 100:.2f}",
                    "discounted_price": f"{game["final_price"] / 100:.2f}",
                    "original_price_usd": f"{game["original_price"] / 100 / USD_EXCHANGE_RATE:.2f}",
                    "discounted_price_usd": f"{game["final_price"] / 100 / USD_EXCHANGE_RATE:.2f}",
                    "discount": game["discount_percent"],
                    "url": f"https://store.steampowered.com/app/{game['id']}/",
                    "image": f"https://cdn.akamai.steamstatic.com/steam/apps/{game['id']}/header.jpg"
                }
                for game in data.get("specials", {}).get("items", []) if game.get("discount_percent", 0) >= 20
            ]



# ========================== ЗАПУСК БОТА ========================== #
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())