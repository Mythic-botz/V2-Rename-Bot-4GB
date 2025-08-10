import os
from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import *  # Import variables directly
from aiohttp import web
from route import web_server
import pyromod
import pyrogram.utils

# Fix for channel/chat id edge cases
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# Optional: user session app (string session)
try:
    from plugins.cb_data import app as Client2
except Exception:
    Client2 = None

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        # Use Client2 only if STRING_SESSION is provided
        self.user_client = Client2 if (STRING_SESSION and Client2) else None

    async def start(self):
        # Start main bot
        await super().start()

        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = BOT_UPTIME if "BOT_UPTIME" in globals() else None

        # Start user session (if available)
        if self.user_client:
            try:
                await self.user_client.start()
                print("✅ User STRING_SESSION started.")
            except Exception as e:
                print(f"[WARN] Could not start user session: {e}")

        # Webhook mode
        if WEBHOOK:
            port = int(os.environ.get("PORT", 8080))
            app_runner = web.AppRunner(await web_server(self))
            await app_runner.setup()
            await web.TCPSite(app_runner, "0.0.0.0", port).start()
            print(f"✅ Web server started on port {port} (WEBHOOK mode).")

        print(f"{me.first_name} is started.....✨️")

        # Notify admins
        for admin_id in ADMIN:
            try:
                await self.send_message(admin_id, f"**{me.first_name} is Started...**")
            except Exception:
                pass

        # Send startup log to log channel
        if LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(
                    LOG_CHANNEL,
                    f"**{self.mention} is Restarted !!**\n\n"
                    f"📅 Date : `{date}`\n"
                    f"⏰ Time : `{time}`\n"
                    f"🌐 Timezone : `Asia/Kolkata`\n\n"
                    f"🉐 Version : `v{__version__} (Layer {layer})`"
                )
            except Exception:
                print("Please make the bot an admin in your log channel.")

    async def stop(self, *args):
        # Stop user session first (if started)
        if self.user_client:
            try:
                await self.user_client.stop()
                print("✅ User STRING_SESSION stopped.")
            except Exception as e:
                print(f"[WARN] Could not stop user session cleanly: {e}")

        await super().stop()

if __name__ == "__main__":
    Bot().run()