import os
from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server   # expects an async def web_server(bot) -> aiohttp.web.Application
import pyromod
import pyrogram.utils

# Fix for channel/chat id edge cases
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# optional: user session app (string session) — your plugins/cb_data should expose `app`
try:
    from plugins.cb_data import app as Client2
except Exception:
    Client2 = None

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        # use Client2 only if a string session is provided and plugins.cb_data exported app
        self.user_client = Client2 if (getattr(Config, "STRING_SESSION", None) and Client2) else None

    async def start(self):
        # start main bot
        await super().start()

        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = getattr(Config, "BOT_UPTIME", None)

        # start user session (if available)
        if self.user_client:
            try:
                await self.user_client.start()
                print("✅ User STRING_SESSION started.")
            except Exception as e:
                print(f"[WARN] Could not start user session: {e}")

        # If using webhook mode, start the aiohttp server and bind to Render PORT
        if getattr(Config, "WEBHOOK", False):
            port = int(os.environ.get("PORT", 8080))
            app_runner = web.AppRunner(await web_server(self))
            await app_runner.setup()
            await web.TCPSite(app_runner, "0.0.0.0", port).start()
            print(f"✅ Web server started on port {port} (WEBHOOK mode).")

        print(f"{me.first_name} is started.....✨️")

        # notify admins
        for admin_id in getattr(Config, "ADMIN", []):
            try:
                await self.send_message(admin_id, f"**{me.first_name} is Started...**")
            except Exception:
                pass

        # send startup log to log channel
        if getattr(Config, "LOG_CHANNEL", None):
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"**{self.mention} is Restarted !!**\n\n📅 Date : `{date}`\n⏰ Time : `{time}`\n🌐 Timezone : `Asia/Kolkata`\n\n🉐 Version : `v{__version__} (Layer {layer})`"
                )
            except Exception:
                print("Please make the bot an admin in your log channel.")

    async def stop(self, *args):
        # stop user session first (if started)
        if self.user_client:
            try:
                await self.user_client.stop()
                print("✅ User STRING_SESSION stopped.")
            except Exception as e:
                print(f"[WARN] Could not stop user session cleanly: {e}")

        await super().stop()

if __name__ == "__main__":
    Bot().run()