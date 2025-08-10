from pyrogram import Client
from config import *
import pyrogram.utils
import pyromod

from plugins.cb_data import app as Client2
from route import main_route, app as flask_app  # Import your Flask/FastAPI app

# ⚙️ Patch minimum chat/channel IDs
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

bot = Client(
    "Renamer",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="plugins")
)

async def startup_log():
    try:
        if LOG_CHANNEL:
            await bot.send_message(
                chat_id=LOG_CHANNEL,
                text="✅ Bot Started Successfully in Webhook Mode!\n\n📡 Powered by @Mythic_Bots"
            )
    except Exception as e:
        print(f"[ERROR] Couldn't send log message: {e}")

async def start_all():
    # Start Pyrogram bot
    await bot.start()
    if STRING_SESSION:
        await Client2.start()

    # Set webhook URL
    webhook_url = f"{BASE_URL}/{WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url)

    await startup_log()

    # Start Flask/FastAPI server (this will keep the process alive)
    main_route(bot)  # Pass bot to route handler so it can process updates

# 🧠 Run the bot in webhook mode
if __name__ == "__main__":
    import asyncio
    asyncio.run(start_all())