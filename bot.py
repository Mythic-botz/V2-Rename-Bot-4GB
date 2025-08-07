from pyrogram import Client, idle
from config import *
import pyrogram.utils
import pyromod

from plugins.cb_data import app as Client2  # ✅ Secondary client (for userbot)
from route import main_route  # ✅ Import main_route to bind webhook route

# ✅ Fix for large channel IDs
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# ✅ Main bot client
bot = Client(
    "Renamer",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="plugins")
)

# ✅ Start all clients (used for webhook deployment like Render)
async def start_all():
    await bot.start()
    if STRING_SESSION:
        await Client2.start()

    main_route()  # ✅ Bind route after clients start
    await idle()

    await bot.stop()
    if STRING_SESSION:
        await Client2.stop()

# ✅ Fallback to run() if not using webhook or userbot
if __name__ == "__main__":
    import asyncio

    if STRING_SESSION:
        asyncio.run(start_all())
    else:
        bot.run()