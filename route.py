from flask import Flask, request
import asyncio
import os
from config import WEBHOOK_PATH  # Import your webhook path from config

app = Flask(__name__)

def main_route(bot):
    @app.route(f"/{WEBHOOK_PATH}", methods=["POST"])
    def webhook():
        try:
            update = request.get_json(force=True)
            asyncio.create_task(
                bot.process_webhook_update(update, request.headers)
            )
        except Exception as e:
            print(f"[ERROR] Webhook processing failed: {e}")
        return "OK", 200
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)