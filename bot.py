import os
import asyncio
from pyrogram import Client
from plugins.cb_data import app as Client2
from config import *
import pyromod
import pyrogram.utils
from aiohttp import web
from route import web_server  # make sure route.py exists

# 🧱 Pyrogram constants
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# 🌐 Render port
PORT = int(os.environ.get("PORT", 8080))

# 🧠 Create main bot client
bot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))


async def start_all():
    print("🚀 Starting Rename Bot...")

    # ✅ Start userbot if STRING_SESSION is set
    if STRING_SESSION:
        try:
            await Client2.start()
            print("✅ Client2 (userbot) started")
        except Exception as e:
            print(f"❌ Error starting Client2: {e}")

    # ✅ Always start main bot
    await bot.start()
    print("✅ Main bot started")

    # 🌐 Start webhook server for Render
    if WEBHOOK:
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()
        print(f"🌐 Webhook server running on port {PORT}")

    me = await bot.get_me()
    print(f"🤖 Bot @{me.username} is running!")


async def stop_all():
    # ⛔ Stop both clients safely
    if STRING_SESSION:
        await Client2.stop()
    await bot.stop()
    print("🛑 Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(start_all())
    except (KeyboardInterrupt, SystemExit):
        asyncio.run(stop_all())