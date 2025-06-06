from telegram.ext import Application, CommandHandler
from aiohttp import web
import os

TOKEN = "8007112570:AAEO65r0kq6nGD0UrFhIltcLZy-EVDVHOiY"
ADMIN_USERNAME = "packoa"
PORT = int(os.environ.get("PORT", 10000))

# Store chat IDs
CHATS = set()

# Create web app
app = web.Application()

async def webhook_handler(request):
    try:
        update = await request.json()
        await application.process_update(update)
        return web.Response(status=200)
    except:
        return web.Response(status=500)

async def start(update, context):
    chat_id = update.effective_chat.id
    CHATS.add(chat_id)
    
    if update.effective_user.username == ADMIN_USERNAME:
        await update.message.reply_text("Admin Commands:\n/broadcast - Send message\n/stats - View stats")
    else:
        await update.message.reply_text("Welcome!")

async def broadcast(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
        
    message = " ".join(context.args)
    success = 0
    failed = 0
    
    for chat_id in CHATS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
            success += 1
        except:
            failed += 1
    
    await update.message.reply_text(f"Sent to {success} users")

async def stats(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    await update.message.reply_text(f"Total users: {len(CHATS)}")

async def setup_webhook():
    webhook_url = os.environ.get("RENDER_EXTERNAL_URL", "https://your-app-name.onrender.com")
    webhook_path = f"/webhook/{TOKEN}"
    await application.bot.set_webhook(url=f"{webhook_url}{webhook_path}")
    return webhook_path

async def main():
    global application
    
    # Initialize bot
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("stats", stats))
    
    # Setup webhook
    webhook_path = await setup_webhook()
    app.router.add_post(webhook_path, webhook_handler)
    
    # Setup health check
    app.router.add_get("/", lambda r: web.Response(text="Bot is running!"))
    
    # Start web server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    
    print(f"Bot is running on port {PORT}")
    await site.start()
    
    # Keep the application running
    while True:
        await asyncio.sleep(3600)  # Sleep for an hour

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
