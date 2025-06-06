from telegram.ext import Application, CommandHandler
import logging
import sys

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8007112570:AAEO65r0kq6nGD0UrFhIltcLZy-EVDVHOiY"
ADMIN_USERNAME = "packoa"

# Store chat IDs
CHATS = set()

async def start(update, context):
    chat_id = update.effective_chat.id
    CHATS.add(chat_id)
    logger.info(f"New chat added: {chat_id}")
    
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
            logger.info(f"Message sent to {chat_id}")
        except Exception as e:
            failed += 1
            logger.error(f"Failed to send to {chat_id}: {e}")
    
    await update.message.reply_text(f"Message sent to {success} users")

async def stats(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    await update.message.reply_text(f"Total subscribers: {len(CHATS)}")

def main():
    try:
        # Initialize bot with specific settings
        application = (
            Application.builder()
            .token(TOKEN)
            .concurrent_updates(False)
            .build()
        )
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("broadcast", broadcast))
        application.add_handler(CommandHandler("stats", stats))
        
        # Start the bot
        logger.info("Starting bot...")
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=["message"]
        )
        
    except Exception as e:
        logger.error(f"Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
