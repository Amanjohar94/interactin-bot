from flask import Flask, request, abort
import razorpay
import hmac
import hashlib
import os
import logging
from telegram import Bot

# Flask app instance
app = Flask(__name__)

# Telegram bot config
BOT_TOKEN = os.getenv("BOT_TOKEN")
VIP_GROUP_ID = int(os.getenv("VIP_GROUP_ID", "-100xxxxxxxxxx"))  # Replace default if needed
bot = Bot(token=BOT_TOKEN)

# Razorpay client config
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Logging
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET"])
def index():
    return "Webhook Server is Live!", 200

@app.route("/razorpay-webhook", methods=["POST"])
def razorpay_webhook():
    try:
        payload = request.data
        received_signature = request.headers.get("X-Razorpay-Signature")
        secret = RAZORPAY_KEY_SECRET.encode()

        # Verify signature
        expected_signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_signature, received_signature):
            logging.warning("Webhook signature verification failed.")
            abort(400)

        data = request.json
        logging.info(f"Webhook received: {data}")

        if data.get("event") == "payment.captured":
            email = data["payload"]["payment"]["entity"].get("email")
            if email:
                message = f"✅ Payment received from {email}. You’ve been granted VIP access!"
            else:
                message = f"✅ Payment captured! You’ve been granted VIP access."

            # Send message to VIP group (or use add_chat_member if needed)
            bot.send_message(chat_id=VIP_GROUP_ID, text=message)

        return "", 200

    except Exception as e:
        logging.error(f"Webhook error: {e}")
        abort(500)

if __name__ == "__main__":
    app.run(debug=True)
