from telegram.ext import Updater, CommandHandler, CallbackContext, ChatJoinRequestHandler
from telegram import Update, ChatJoinRequest

# Replace with your actual Bot Token from @BotFather
BOT_TOKEN = "YOUR_BOT_2_TOKEN"

# Handles /start command in private chat
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Welcome to our Trading Assistant Bot!\n\n"
        "🎯 You’ve been approved to join the public group.\n"
        "💰 Want premium access? Chat here anytime."
    )

# Auto-approve join request to public group
def handle_join_request(update: Update, context: CallbackContext):
    join_request: ChatJoinRequest = update.chat_join_request

    try:
        context.bot.approve_chat_join_request(
            chat_id=join_request.chat.id,
            user_id=join_request.from_user.id
        )

        context.bot.send_message(
            chat_id=join_request.from_user.id,
            text=(
                "✅ You’ve been approved to join our public trading group!\n"
                "🚀 Explore our winning trades and results.\n\n"
                "📩 For premium access, chat here anytime."
            )
        )
    except Exception as e:
        print(f"Error approving user: {e}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(ChatJoinRequestHandler(handle_join_request))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
