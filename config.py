from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

group_id = os.getenv("PUBLIC_GROUP_ID")
vip_id = os.getenv("VIP_GROUP_ID")

PUBLIC_GROUP_ID = int(group_id) if group_id else None
VIP_GROUP_ID = int(vip_id) if vip_id else None
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
