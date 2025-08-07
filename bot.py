import os
from pyrogram import Client
from plugins.cb_data import app as Client2
from config import *
import pyromod
import pyrogram.utils
from aiohttp import web
from datetime import datetime
from route import web_server  # Make sure you have this module (like in 2GB bot)

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

PORT = int(os.environ.get("PORT", 8080))  # Default to 8080 if PORT not set

bot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))


async def start_all():
    print("🚀 Starting 4GB Rename Bot with Webhook...")
    await Client2.start()
    await bot.start()

    # Start webhook server (aiohttp)
    if WEBHOOK:
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()
        print(f"🌐 Webhook server started on port {PORT}")

    me = await bot.get_me()
    print(f"🤖 {me.first_name} (@{me.username}) is running!")
    # Add optional admin notify if needed


async def stop_all():
    await Client2.stop()
    await bot.stop()
    print("🛑 Bot stopped.")


if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(start_all())
    except (KeyboardInterrupt, SystemExit):
        asyncio.run(stop_all())