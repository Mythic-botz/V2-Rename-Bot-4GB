# from aiohttp import web
# import asyncio
# from config import WEBHOOK_PATH  # Import directly

#async def handle_webhook(request):
   # try:
 #       data = await request.json()
#        headers = {k: v for k, v in #request.headers.items()}
        #asyncio.create_task(request.app["bot"].process_web#hook_update(data, headers))
#        return web.Response(text="OK")
#    except Exception as e:
#        print(f"[ERROR] Webhook update failed: #{e}")
#        return web.Response(status=500, #text="Error")

#async def web_server(bot):
 #   app = web.Application()
#    app["bot"] = bot
#    app.router.add_post(f"/{WEBHOOK_PATH}", #handle_webhook)
#    app.router.add_get("/", lambda req: #web.Response(text="Bot is running!"))
#    return app