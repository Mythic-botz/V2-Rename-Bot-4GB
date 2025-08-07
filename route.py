from aiohttp import web

async def web_server():
    async def handle(request):
        return web.Response(text="Bot is running via webhook on Render!", status=200)

    app = web.Application()
    app.router.add_get("/", handle)
    return app