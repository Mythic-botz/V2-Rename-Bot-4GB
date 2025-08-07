# route.py
from fastapi import FastAPI
from pyrogram import Client
from config import WEBHOOK_URL, PORT

import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK", "message": "Bot is running"}

def main_route():
    import threading

    def start_uvicorn():
        uvicorn.run("route:app", host="0.0.0.0", port=PORT, log_level="info")

    threading.Thread(target=start_uvicorn).start()