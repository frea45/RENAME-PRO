from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta
from helper.database import find_user, is_gift_used, activate_gift_plan

@Client.on_message(filters.command("gift") & filters.private)
async def activate_gift_command(bot, message: Message):
    user_id = message.from_user.id
    user_data = await find_user(user_id)

    if not user_data:
        return await message.reply("برای استفاده از ربات ابتدا /start را بزنید.")

    current_plan = user_data.get("plan", "Free")

    if current_plan in ["Silver", "Gold", "Diamond"]:
        return await message.reply("شما هم‌اکنون پلن فعال دارید و نمی‌توانید از پلن هدیه استفاده کنید.")

    if await is_gift_used(user_id):
        return await message.reply("شما قبلاً از پلن هدیه استفاده کرده‌اید.")

    await activate_gift_plan(user_id)
    await message.reply(
        "پلن هدیه یک‌هفته‌ای با حجم روزانه ۵ گیگ برای شما فعال شد!\n"
        "اکنون می‌توانید لینک فایل خود را بفرستید تا آن را تغییر نام دهیم."
    )
