from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import activate_gift_plan_db, get_user_plan
from config import OWNER, LOG_CHANNEL

@Client.on_message(filters.command("gift") & filters.private)
async def activate_gift_plan(client: Client, message: Message):
    user_id = message.from_user.id

    # بررسی اینکه کاربر جزو پلن‌های نقره‌ای، طلایی یا الماسی نباشد
    user_plan = get_user_plan(user_id)
    if user_plan in ["silver", "gold", "diamond"]:
        return await message.reply("شما در حال حاضر دارای پلن فعال هستید و نمی‌توانید از پلن هدیه استفاده کنید.")

    # بررسی اینکه کاربر قبلاً از پلن هدیه استفاده کرده یا نه
    user_data = client.db.users.find_one({"_id": user_id})
    if user_data and user_data.get("gift_used", False):
        return await message.reply("شما قبلاً از پلن هدیه استفاده کرده‌اید.")

    # فعال‌سازی پلن هدیه برای 7 روز
    activate_gift_plan_db(user_id)

    # بروزرسانی وضعیت gift_used برای جلوگیری از استفاده مجدد
    client.db.users.update_one({"_id": user_id}, {"$set": {"gift_used": True}}, upsert=True)

    await message.reply("پلن هدیه 7 روزه با موفقیت برای شما فعال شد!")

    # اطلاع‌رسانی در لاگ
    text = (
        f"پلن GIFT 7 روزه فعال شد.\n"
        f"نام کاربر: {message.from_user.first_name}\n"
        f"آیدی عددی: {user_id}\n"
        f"نام پلن: gift"
    )
    try:
        await client.send_message(LOG_CHANNEL, text)
        # await client.send_message(OWNER, text)  # اگر خواستی به OWNER هم ارسال بشه، این رو از حالت کامنت خارج کن
    except:
        pass
