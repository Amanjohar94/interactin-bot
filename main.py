
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    ChatJoinRequestHandler,
    Filters
)
from telegram import Update, ChatJoinRequest
from config import BOT_TOKEN, PUBLIC_GROUP_ID
from promo_scheduler import send_promos
from payment_flow import handle_private_message
from bot_core.utils.promo_texts import PROMO_WELCOME, PROMO_JOIN, PROMO_CTA

def start(update: Update, context: CallbackContext):
    args = context.args
    if args and args[0] == "vip":
        handle_private_message(update, context)
    else:
        update.message.reply_text(
            PROMO_WELCOME,
            parse_mode='HTML',
            disable_web_page_preview=True
        )

def get_chat_id(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    update.message.reply_text(f"✅ This chat ID is:\n{chat_id}")

def handle_join_request(update: Update, context: CallbackContext):
    join_request: ChatJoinRequest = update.chat_join_request
    try:
        context.bot.approve_chat_join_request(
            chat_id=join_request.chat.id,
            user_id=join_request.from_user.id
        )
        context.bot.send_message(
            chat_id=join_request.from_user.id,
            text=PROMO_JOIN,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"❌ Error approving user: {e}")

def pin_cta_message(context: CallbackContext):
    try:
        context.bot.send_message(
            chat_id=PUBLIC_GROUP_ID,
            text=PROMO_CTA,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"❌ Failed to send CTA message: {e}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("id", get_chat_id))
    dp.add_handler(ChatJoinRequestHandler(handle_join_request))
    dp.add_handler(MessageHandler(Filters.private & Filters.text, handle_private_message))

    print("✅ Bot is running...")
    updater.start_polling()

    if PUBLIC_GROUP_ID:
        send_promos()

    updater.job_queue.run_once(pin_cta_message, 10)
    updater.idle()

if __name__ == '__main__':
    main()