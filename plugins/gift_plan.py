from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta
from helper.database import (
    activate_gift_plan_db,
    get_user_data,
    mark_gift_used,
    has_used_gift
)
from config import LOG_CHANNEL

@Client.on_message(filters.command("gift"))
async def activate_gift_plan(client: Client, message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    if has_used_gift(user_id):
        await message.reply_text("شما قبلاً از پلن هدیه یک‌هفته‌ای استفاده کرده‌اید.")
        return

    # فعالسازی پلن هدیه در دیتابیس
    activate_gift_plan_db(user_id)
    mark_gift_used(user_id)

    await message.reply_text(
        "پلن هدیه با موفقیت برای شما فعال شد!\n"
        "مدت زمان: 7 روز\n"
        "حجم روزانه: 5 گیگابایت\n"
        "لذت ببرید!"
    )

    # ارسال پیام به کانال لاگ
    await client.send_message(
        LOG_CHANNEL,
        f"🎁 پلن هدیه فعال شد!\n\n"
        f"👤 کاربر: {message.from_user.mention}\n"
        f"🆔 آیدی: `{user_id}`\n"
        f"⏳ مدت: 7 روز\n"
        f"📦 حجم روزانه: 5 گیگابایت\n"
        f"📅 تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
