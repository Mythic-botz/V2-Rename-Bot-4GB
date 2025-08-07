import os
import asyncio
from pyrogram import Client
from plugins.cb_data import app as Client2
from aiohttp import web
import pyromod
import pyrogram.utils
from config import *

# Patch for small chat/channel IDs
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# 🔐 Config from env or config.py
API_ID = config.API_ID
API_HASH = config.API_HASH
BOT_TOKEN = os.environ.get("BOT_TOKEN", BOT_TOKEN)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://zenitsu-renamer.onrender.com") # 👆 Render url 
PORT = int(os.environ.get("PORT", 10000))

# 🌐 Main Bot
bot = Client(
    "Renamer",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="plugins")
)

# 🌐 Start a dummy aiohttp server to keep the port alive
async def handle(request):
    return web.Response(text="✅ Webhook is running!")

async def run_webserver():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"🌐 Server running on http://0.0.0.0:{PORT}")

# 🚀 Startup
async def start():
    if STRING_SESSION:
        apps = [Client2, bot]
        for app in apps:
            await app.start()
        await bot.set_webhook(WEBHOOK_URL)
        await run_webserver()
        print("✅ Bot running with webhook.")
        await asyncio.Event().wait()
        for app in apps:
            await app.stop()
    else:
        await bot.start()
        await bot.set_webhook(WEBHOOK_URL)
        await run_webserver()
        print("✅ Bot running with webhook.")
        await asyncio.Event().wait()
        await bot.stop()

# 🧠 Run main
if __name__ == "__main__":
    asyncio.run(start())