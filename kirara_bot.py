from telegram.ext import Application, CommandHandler
from aiohttp import web
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8007112570:AAEO65r0kq6nGD0UrFhIltcLZy-EVDVHOiY"
ADMIN_USERNAME = "packoa"
PORT = int(os.environ.get("PORT", 10000))

# Store chat IDs
CHATS = set()

# Create web app
app = web.Application()

async def webhook_handler(request):
    try:
        data = await request.json()
        await application.process_update(data)
        return web.Response(status=200)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
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
        
    message = ' '.join(context.args)
    success = 0
    failed = 0
    
    for chat_id in CHATS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
            success += 1
        except:
            failed += 1
    
    await update.message.reply_text(f"Message sent to {success} users")

async def stats(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    await update.message.reply_text(f"Total subscribers: {len(CHATS)}")

async def main():
    global application
    
    # Initialize bot
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("stats", stats))
    
    # Setup webhook
    webhook_url = "https://kirara-bot-2.onrender.com"
    webhook_path = f"/webhook/{TOKEN}"
    await application.bot.set_webhook(url=f"{webhook_url}{webhook_path}")
    
    # Add routes
    app.router.add_post(webhook_path, webhook_handler)
    app.router.add_get("/", lambda r: web.Response(text="Bot is running!"))
    
    # Start web server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    
    logger.info(f"Bot started on port {PORT}")
    
    # Keep alive
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
