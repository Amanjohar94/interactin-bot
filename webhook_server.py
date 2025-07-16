from flask import Flask, request
import razorpay
from telegram import Bot
from config import BOT_TOKEN, VIP_GROUP_ID, RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

@app.route("/razorpay-webhook", methods=["POST"])
def razorpay_webhook():
    payload = request.get_data(as_text=True)
    signature = request.headers.get("X-Razorpay-Signature")

    try:
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        client.utility.verify_webhook_signature(payload, signature, RAZORPAY_KEY_SECRET)

        data = request.json
        entity = data.get("payload", {}).get("payment_link", {}).get("entity", {})
        telegram_user_id = int(entity.get("notes", {}).get("telegram_user_id"))

        bot.invite_chat_member(chat_id=VIP_GROUP_ID, user_id=telegram_user_id)
        bot.send_message(chat_id=telegram_user_id, text="✅ Payment confirmed! You’ve been added to VIP 🚀")

        return "OK", 200
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return "Error", 400

if __name__ == "__main__":
    app.run(port=5000)
