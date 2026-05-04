import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import web

TOKEN = os.getenv("TOKEN")
PAYEER_ACCOUNT = os.getenv("PAYEER_ACCOUNT") 
PAYEER_API_KEY = os.getenv("PAYEER_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 VIP олиш - 1$", callback_data="buy_vip")]
    ])
    await message.answer("Салом! VIP олиш учун кнопкани бос:", reply_markup=kb)

@dp.callback_query(F.data == "buy_vip")
async def buy_vip(call: types.CallbackQuery):
    order_id = call.from_user.id
    desc = f"VIP_{order_id}"
    pay_url = f"https://payeer.com/merchant/?m_shop={PAYEER_ACCOUNT}&m_orderid={order_id}&m_amount=1.00&m_curr=USD&m_desc={desc}&lang=ru"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Тўлаш Payeer", url=pay_url)]
    ])
    await call.message.answer(f"1$ тўлов учун ссылка:\n{pay_url}", reply_markup=kb)
    await call.answer()

async def handle(request):
    return web.Response(text="Bot is running!")

async def start_bot():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
#   deploy
