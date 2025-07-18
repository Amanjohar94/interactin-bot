import threading
from telegram import Bot
from config import BOT_TOKEN, PUBLIC_GROUP_ID

bot = Bot(token=BOT_TOKEN)

# 👇 Updated marketing messages (link to your bot)
messages = [
    "🚀 *Today’s Profit:* +₹5,200 on EUR/USD scalping!\nWant real-time signals? 👉 [Join VIP](https://t.me/tradejoinbot)",
    "📊 VIPs made ₹15,000 this week with our live signals!\n👉 [Click to Join VIP](https://t.me/tradejoinbot)",
    "💰 *95% Accuracy?* It’s not hype. It’s data.\n[Unlock Premium Access](https://t.me/tradejoinbot)",
    "🔥 Missed 3 wins today?\nDon’t miss the next.\n[Join Now](https://t.me/tradejoinbot)"
]

import asyncio

async def send_promos(index=0):
    try:
        message = messages[index % len(messages)]
        await bot.send_message(
            chat_id=PUBLIC_GROUP_ID,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        print(f"✅ Sent promo: {message}")
    except Exception as e:
        print(f"❌ Failed to send promo: {e}")

    # Send every 3 hours (10800 sec)
    asyncio.get_event_loop().call_later(10800, lambda: asyncio.create_task(send_promos(index + 1)))
