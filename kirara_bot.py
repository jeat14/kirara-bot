from telegram.ext import Application, CommandHandler
import logging
import sys
import json
from datetime import datetime

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8007112570:AAEZk2UqEp_HqCFYUKF7s0vM2gr4JEJLUP0"  # Replace with your actual token
ADMIN_USERNAME = "packoa"

# Store user data
USERS = {}  # {chat_id: {'username': str, 'joined': str, 'status': 'active/blocked'}}

async def start(update, context):
    chat_id = update.effective_chat.id
    username = update.effective_user.username or "Unknown"
    
    USERS[str(chat_id)] = {
        'username': username,
        'joined': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'active'
    }
    
    if update.effective_user.username == ADMIN_USERNAME:
        await update.message.reply_text(
            "🔰 Admin Commands:\n\n"
            "📢 /broadcast - Send text message\n"
            "🎥 /sendvideo - Send video (Reply to video)\n"
            "📊 /stats - View detailed stats\n"
            "👥 /users - List all users\n"
            "🚫 /block <user_id> - Block user\n"
            "✅ /unblock <user_id> - Unblock user"
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
    
    for chat_id, user in USERS.items():
        if user['status'] == 'active':
            try:
                await context.bot.send_message(chat_id=int(chat_id), text=message)
                success += 1
            except Exception as e:
                failed += 1
                logger.error(f"Failed to send to {chat_id}: {e}")
    
    await update.message.reply_text(f"✅ Sent to {success} users\n❌ Failed: {failed}")

async def send_video(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    
    if not update.message.reply_to_message or not update.message.reply_to_message.video:
        await update.message.reply_text("Reply to a video with /sendvideo [caption]")
        return

    video = update.message.reply_to_message.video
    caption = ' '.join(context.args) if context.args else None
    
    success = 0
    failed = 0
    
    for chat_id, user in USERS.items():
        if user['status'] == 'active':
            try:
                await context.bot.send_video(
                    chat_id=int(chat_id),
                    video=video.file_id,
                    caption=caption
                )
                success += 1
            except Exception as e:
                failed += 1
                logger.error(f"Failed to send video to {chat_id}: {e}")
    
    await update.message.reply_text(f"✅ Video sent to {success} users\n❌ Failed: {failed}")

async def stats(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    
    total_users = len(USERS)
    active_users = sum(1 for user in USERS.values() if user['status'] == 'active')
    blocked_users = sum(1 for user in USERS.values() if user['status'] == 'blocked')
    
    stats_msg = (
        "📊 Bot Statistics\n\n"
        f"Total Users: {total_users}\n"
        f"Active Users: {active_users}\n"
        f"Blocked Users: {blocked_users}"
    )
    
    await update.message.reply_text(stats_msg)

async def list_users(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    
    if not USERS:
        await update.message.reply_text("No users yet!")
        return
    
    user_list = "👥 User List:\n\n"
    for chat_id, user in USERS.items():
        status = "✅" if user['status'] == 'active' else "🚫"
        user_list += f"{status} {user['username']} (ID: {chat_id})\n"
        user_list += f"Joined: {user['joined']}\n\n"
    
    await update.message.reply_text(user_list)

async def block_user(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /block <user_id>")
        return
    
    user_id = context.args[0]
    if user_id in USERS:
        USERS[user_id]['status'] = 'blocked'
        await update.message.reply_text(f"User {USERS[user_id]['username']} blocked!")
    else:
        await update.message.reply_text("User not found!")

async def unblock_user(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /unblock <user_id>")
        return
    
    user_id = context.args[0]
    if user_id in USERS:
        USERS[user_id]['status'] = 'active'
        await update.message.reply_text(f"User {USERS[user_id]['username']} unblocked!")
    else:
        await update.message.reply_text("User not found!")

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
        application.add_handler(CommandHandler("sendvideo", send_video))
        application.add_handler(CommandHandler("stats", stats))
        application.add_handler(CommandHandler("users", list_users))
        application.add_handler(CommandHandler("block", block_user))
        application.add_handler(CommandHandler("unblock", unblock_user))
        
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
