from pyrogram import Client
from config import *
import pyrogram.utils
import pyromod

from plugins.cb_data import app as Client2
from route import main_route  # Import only the route starter

# ⚙️ Patch minimum chat/channel IDs
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# 📦 Main Pyrogram Bot Client
bot = Client(
    "Renamer",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="plugins")
)

# 📜 Send a startup log to LOG_CHANNEL
async def startup_log():
    try:
        if LOG_CHANNEL:
            await bot.send_message(
                chat_id=LOG_CHANNEL,
                text="✅ Bot Started Successfully in Webhook Mode!\n\n📡 Powered by @Mythic_Bots"
            )
    except Exception as e:
        print(f"[ERROR] Couldn't send log message: {e}")

# 🚀 Start bot and web server
async def start_all():
    await bot.start()
    if STRING_SESSION:
        await Client2.start()

    await startup_log()

    # Start the Flask/FastAPI server (keeps the process alive)
    main_route(bot)  # Pass the bot so it can handle updates

# 🧠 Entry point
if __name__ == "__main__":
    import asyncio
    asyncio.run(start_all())