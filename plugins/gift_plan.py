from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import find_one, activate_gift_plan_db, has_used_gift
import time
from config import LOG_CHANNEL, ADMIN

@Client.on_message(filters.private & filters.command("gift"))
async def activate_gift_plan(client, message: Message):
    user_id = message.from_user.id
    user_data = find_one(user_id)

    if not user_data:
        await message.reply("ابتدا /start را ارسال کنید.")
        return

    current_plan = user_data.get("usertype", "Free")
    if current_plan in ["Silver", "Gold", "Diamond"]:
        await message.reply("شما پلن فعال دارید و نمی‌توانید از پلن هدیه استفاده کنید.")
        return

    if has_used_gift(user_id):
        await message.reply("شما قبلاً از پلن هدیه استفاده کرده‌اید.")
        return

    # فعال‌سازی پلن هدیه
    update_user_plan(
        user_id=user_id,
        upload_limit=5 * 1024 * 1024 * 1024,  # 5 گیگ
        user_type="Gift",
        days=7
    )

    await message.reply("پلن هدیه ۷ روزه با موفقیت برای شما فعال شد. حجم روزانه: ۵ گیگ")

    # اطلاع‌رسانی در کانال لاگ و (ارسال به ادمین کامنت شده)
    try:
        user_mention = f"{message.from_user.mention}"
        log_text = (
            f"پلن هدیه فعال شد.\n"
            f"نام کاربر: {user_mention}\n"
            f"آیدی عددی: `{user_id}`\n"
            f"نام پلن: Gift"
        )
        await client.send_message(LOG_CHANNEL, log_text)
        # await client.send_message(int(ADMIN), log_text)  # ارسال به ادمین (کامنت شده)
    except Exception as e:
        print(f"خطا در ارسال به لاگ یا ادمین: {e}")
