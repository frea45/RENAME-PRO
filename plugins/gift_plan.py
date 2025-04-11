from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import find_one, update_user_plan2

@Client.on_message(filters.command("gift") & filters.private)
async def gift_plan_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_data = await find_one(user_id)

    if not user_data:
        return await message.reply("لطفاً ابتدا با استفاده از /start ثبت‌نام کنید.")

    current_plan = user_data.get("usertype", "Free")
    if current_plan in ["Silver", "Gold", "Diamond"]:
        return await message.reply("شما قبلاً پلن فعال دارید و نمی‌توانید از پلن هدیه استفاده کنید.")

    if user_data.get("gift_used"):
        return await message.reply("شما قبلاً از پلن هدیه استفاده کرده‌اید.")

    result = await update_user_plan2(
        user_id=user_id,
        usertype="7days",
        daily_limit=5 * 1024 * 1024 * 1024,  # 5 گیگ
        days=7
    )

    if result == "success":
        from helper.database import update_one
        await update_one(user_id, {"gift_used": True})
        await message.reply("پلن هدیه ۷ روزه با موفقیت برای شما فعال شد.\nروزانه 5 گیگ محدودیت دارید.")
    else:
        await message.reply("خطا در فعال‌سازی پلن هدیه. لطفاً دوباره تلاش کنید.")
