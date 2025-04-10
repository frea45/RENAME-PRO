import time
from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import find_one, update_user_plan, has_used_gift, set_gift_used

GIFT_UPLOAD_LIMIT = 5 * 1024 * 1024 * 1024  # 5GB
GIFT_DURATION_DAYS = 7

@Client.on_message(filters.private & filters.command("gift"))
async def gift_plan(client, message: Message):
    user_id = message.from_user.id
    user_data = find_one(user_id)

    if not user_data:
        await message.reply("لطفاً ابتدا /start را ارسال کنید.")
        return

    if user_data["usertype"] in ["Silver", "Gold", "Diamond"]:
        await message.reply("شما قبلاً پلن ارتقاء یافته دارید و نمی‌توانید از پلن هدیه استفاده کنید.")
        return

    if has_used_gift(user_id):
        await message.reply("شما قبلاً از پلن هدیه استفاده کرده‌اید و امکان استفاده مجدد وجود ندارد.")
        return

    # فعال‌سازی پلن هدیه
    update_user_plan(user_id, GIFT_UPLOAD_LIMIT, "Vip", GIFT_DURATION_DAYS)
    set_gift_used(user_id)
    await message.reply("پلن هدیه با موفقیت برای شما فعال شد! به مدت 7 روز، روزانه 5 گیگابایت حجم دارید.")
