
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ChatJoinRequestHandler,
    filters
)
from telegram import Update, ChatJoinRequest
from config import BOT_TOKEN, PUBLIC_GROUP_ID
from promo_scheduler import send_promos
from payment_flow import handle_private_message
from bot_core.utils.promo_texts import PROMO_WELCOME, PROMO_JOIN, PROMO_CTA

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args and args[0] == "vip":
        await handle_private_message(update, context)
    else:
        await update.message.reply_text(
            PROMO_WELCOME,
            parse_mode='HTML',
            disable_web_page_preview=True
        )

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"✅ This chat ID is:\n{chat_id}")

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_request: ChatJoinRequest = update.chat_join_request
    try:
        await context.bot.approve_chat_join_request(
            chat_id=join_request.chat.id,
            user_id=join_request.from_user.id
        )
        await context.bot.send_message(
            chat_id=join_request.from_user.id,
            text=PROMO_JOIN,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"❌ Error approving user: {e}")

async def pin_cta_message(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(
            chat_id=PUBLIC_GROUP_ID,
            text=PROMO_CTA,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"❌ Failed to send CTA message: {e}")

async def main():
    def on_startup(app):
        app.job_queue.run_once(pin_cta_message, 10)

    application = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("id", get_chat_id))
    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, handle_private_message))

    print("✅ Bot is running...")

    if PUBLIC_GROUP_ID:
        send_promos()

    await application.run_polling()

import asyncio

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "Cannot close a running event loop" in str(e):
            pass  # PTB manages the event loop, safe to ignore
        else:
            raise