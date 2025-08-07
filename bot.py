from pyrogram import Client, idle
from config import *
import pyrogram.utils
import pyromod

from plugins.cb_data import app as Client2
from route import main_route  # ✅ Import route.py main function

# ⚙️ Patch minimum chat/channel IDs (rare issue fix)
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# 📦 Create Pyrogram Bot Client
bot = Client(
    "Renamer",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root='plugins')
)

async def startup_log():
    try:
        if LOG_CHANNEL:
            await bot.send_message(
                chat_id=LOG_CHANNEL,
                text="✅ Bot Started Successfully!\n\n📡 Powered by @Mythic_Bots"
            )
    except Exception as e:
        print(f"[ERROR] Couldn't send log message: {e}")

# 🚀 Main App Runner
async def start_all():
    await bot.start()
    if STRING_SESSION:
        await Client2.start()
    await startup_log()     # ✅ Send log message
    main_route()            # ✅ Execute route functions (like webhook path binders)
    await idle()            # ♻️ Keep the bot alive
    await bot.stop()
    if STRING_SESSION:
        await Client2.stop()

# 🧠 Run the bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(start_all())

# 🙏 Do Not Remove Credits
# Made by @VoidxTora | @Mythic_Bots | @