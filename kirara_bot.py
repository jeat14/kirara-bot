from telegram.ext import Application, CommandHandler
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8007112570:AAEO65r0kq6nGD0UrFhIltcLZy-EVDVHOiY"
ADMIN_USERNAME = "packoa"

# Store chat IDs
CHATS = set()

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

def main():
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("stats", stats))
    
    # Start bot
    logger.info("Starting bot...")
    application.run_polling(poll_interval=3.0, drop_pending_updates=True)
    logger.info("Bot stopped")

if __name__ == "__main__":
    main()
