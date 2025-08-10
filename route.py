from flask import Flask, request
import asyncio

app = Flask(__name__)

def main_route(bot):
    @app.route(f"/{WEBHOOK_PATH}", methods=["POST"])
    def webhook():
        update = request.get_json(force=True)
        asyncio.create_task(bot.process_webhook_update(update))
        return "OK", 200

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)