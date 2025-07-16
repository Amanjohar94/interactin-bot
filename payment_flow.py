import razorpay
from telegram import ParseMode
from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def generate_payment_link(telegram_user_id):
    payment = client.payment_link.create({
        "amount": 99900,  # ₹999 in paise
        "currency": "INR",
        "description": "VIP Membership - Trading Signals",
        "callback_url": "https://your-ngrok-url/razorpay-webhook",  # Replace when ngrok runs
        "callback_method": "get",
        "notes": {
            "telegram_user_id": str(telegram_user_id)
        }
    })
    return payment["short_url"]

def handle_private_message(update, context):
    telegram_user_id = update.effective_user.id
    payment_link = generate_payment_link(telegram_user_id)

    message = (
        "📋 *VIP Membership Plans:*\n\n"
        "1️⃣ ₹999/month - Real-time Premium Signals\n\n"
        f"👉 [Click here to Pay]({payment_link})\n\n"
        "✅ After payment, you'll be added to our VIP group automatically!"
    )

    context.bot.send_message(
        chat_id=telegram_user_id,
        text=message,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

