from telegram.ext import Application, CommandHandler
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8007112570:AAEO65r0kq6nGD0UrFhIltcLZy-EVDVHOiY"
ADMIN_USERNAME = "packoa"

# Store chat IDs and user info
USERS = {}  # {chat_id: {"username": username, "joined": datetime}}

async def start(update, context):
    chat_id = update.effective_chat.id
    username = update.effective_user.username or "Unknown"
    
    # Store user info
    USERS[chat_id] = {
        "username": username,
        "joined": datetime.now()
    }
    
    if update.effective_user.username == ADMIN_USERNAME:
        await update.message.reply_text(
            "🔰 Admin Commands:\n\n"
            "📢 /broadcast - Send message to all users\n"
            "📊 /stats - View detailed statistics\n"
            "👥 /users - List all users\n"
            "📝 /announce - Send formatted announcement"
        )
    else:
        await update.message.reply_text("Welcome! You will receive updates.")

async def broadcast(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
        
    message = ' '.join(context.args)
    success = 0
    failed = 0
    
    for chat_id in USERS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
            success += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed to send to {chat_id}: {e}")
    
    await update.message.reply_text(f"✅ Sent to {success} users\n❌ Failed: {failed}")

async def announce(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /announce <message>")
        return
        
    message = ' '.join(context.args)
    formatted_message = (
        "📢 ANNOUNCEMENT\n"
        "━━━━━━━━━━━━━━━\n\n"
        f"{message}\n\n"
        "━━━━━━━━━━━━━━━"
    )
    
    success = 0
    failed = 0
    
    for chat_id in USERS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=formatted_message)
            success += 1
        except:
            failed += 1
    
    await update.message.reply_text(f"✅ Announcement sent to {success} users\n❌ Failed: {failed}")

async def stats(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    
    total_users = len(USERS)
    
    # Get users who joined today
    today = datetime.now().date()
    new_users = sum(1 for user in USERS.values() 
                   if user["joined"].date() == today)
    
    stats_message = (
        "📊 Bot Statistics\n"
        "━━━━━━━━━━━━━━━\n\n"
        f"Total Users: {total_users}\n"
        f"New Today: {new_users}\n"
        "━━━━━━━━━━━━━━━"
    )
    
    await update.message.reply_text(stats_message)

async def list_users(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    
    if not USERS:
        await update.message.reply_text("No users yet!")
        return
    
    user_list = "👥 User List\n━━━━━━━━━━━━━━━\n\n"
    
    for chat_id, info in USERS.items():
        username = info["username"]
        joined = info["joined"].strftime("%Y-%m-%d")
        user_list += f"• {username}\n  Joined: {joined}\n"
    
    await update.message.reply_text(user_list)

def main():
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("announce", announce))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("users", list_users))
    
    # Start bot
    logger.info("Starting bot...")
    application.run_polling(poll_interval=1.0)
    logger.info("Bot stopped")

if __name__ == "__main__":
    main()
