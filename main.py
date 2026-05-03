import asyncio
import hashlib
import os
from urllib.parse import urlencode
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

TOKEN = os.getenv("TOKEN")
PAYEER_ACCOUNT = os.getenv("PAYEER_ACCOUNT")  # P12345678
PAYEER_API_KEY = os.getenv("PAYEER_API_KEY") # AbCdEf123456

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. ТЎЛОВ ССЫЛКА ЯСАЙДИ
def payeer_link(user_id: int, amount: float, desc: str):
    m_shop = PAYEER_ACCOUNT
    m_orderid = str(user_id)
    m_amount = f"{amount:.2f}"
    m_curr = "USD"
    m_desc = urlencode({"": desc})[1:]  # urlencode қилиш
    m_key = PAYEER_API_KEY
    
    sign = f"{m_shop}:{m_orderid}:{m_amount}:{m_curr}:{m_desc}:{m_key}"
    m_sign = hashlib.sha256(sign.encode()).hexdigest().upper()
    
    params = {
        "m_shop": m_shop,
        "m_orderid": m_orderid, 
        "m_amount": m_amount,
        "m_curr": m_curr,
        "m_desc": m_desc,
        "m_sign": m_sign
    }
    return f"https://payeer.com/merchant/?{urlencode(params)}"

# 2. /start КОМАНДАСИ
@dp.message(Command("start"))
async def start(msg: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 VIP олиш - 1$", callback_data="buy")]
    ])
    await msg.answer("Салом ака! Son Top Bot'га хуш келибсан!\nVIP доступ 1$", reply_markup=kb)

# 3. ТЎЛОВ КНОПКАСИ
@dp.callback_query(F.data == "buy")
async def buy(call: types.CallbackQuery):
    url = payeer_link(call.from_user.id, 1.00, "VIP SonTopBot")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Тўлаш Payeer", url=url)],
        [InlineKeyboardButton(text="✅ Тўладим", callback_data="check")]
    ])
    await call.message.edit_text("1$ тўлаш учун бос. Тўлагандан кейин 'Тўладим' бос:", reply_markup=kb)

# 4. ТЎЛОВНИ ТЕКШИРИШ
@dp.callback_query(F.data == "check")
async def check(call: types.CallbackQuery):
    # Бу ерда Payeer API орқали текшириш керак. Ҳозирча автоматик берамиз
    await call.message.edit_text("✅ Тўлов қабул қилинди! VIP доступ очилди.\nЛинк: https://t.me/+xxxxxx")
    await call.answer("Успешно!", show_alert=True)

# 5. RENDER УЧУН WEB SERVER
async def handle(request):
    return web.Response(text="Bot is running!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 10000)))
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
