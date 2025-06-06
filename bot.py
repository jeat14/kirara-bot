from telegram.ext import Application, CommandHandler

TOKEN = "8007112570:AAEO65r0kq6nGD0UrFhIltcLZy-EVDVHOiY"
ADMIN_USERNAME = "packoa"

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

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("stats", stats))
    
    print("Bot running...")
    app.run_polling(poll_interval=1.0)

if __name__ == "__main__":
    main()
