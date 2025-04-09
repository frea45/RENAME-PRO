import random
import string
from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER
from helper.database import find_one, add_vip_code, use_vip_code, update_user_plan


# تولید کد VIP یکبار مصرف توسط ادمین
@Client.on_message(filters.private & filters.command("crate_vip"))
async def create_vip_code(client: Client, message: Message):
    if message.from_user.id not in OWNER:
        return await message.reply("شما اجازه استفاده از این دستور را ندارید.")
    
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    add_vip_code(code)
    await message.reply(f"کد VIP با موفقیت ساخته شد:\n\n`{code}`\n\nاین کد فقط یک‌بار قابل استفاده است.")

# فعالسازی پلن VIP توسط کاربر
"""
@Client.on_message(filters.private & filters.command("vip"))
async def use_vip(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("لطفاً کد VIP را به صورت صحیح وارد کنید.\n\nمثال:\n`/vip ABCD1234`")
    
    code = message.command[1]
    used = use_vip_code(code)
    if not used:
        return await message.reply("کد نامعتبر یا قبلاً استفاده شده است.")

    update_user_plan(message.from_user.id, plan_type="VIP", days=15, daily_limit=5 * 1024**3)
    await message.reply("پلن VIP با موفقیت فعال شد!\nمدت: 15 روز\nحجم روزانه: 5 گیگابایت\nبدون محدودیت حجم فایل.") """

@Client.on_message(filters.private & filters.command("vip"))
async def redeem_vip_code(client, message: Message):
    user_id = message.from_user.id
    user_data = find_one(user_id)

    if not user_data:
        await message.reply("ابتدا /start را ارسال کنید.")
        return


    usertype = user_data.get("usertype", "Free").lower()

    if usertype != "Free":
        await message.reply("فقط کاربران با پلن رایگان می‌توانند از کد VIP استفاده کنند.")
        print("Usertype:", user_data.get("usertype"))

        return

    if len(message.command) < 2:
        await message.reply("لطفاً کد VIP را به صورت زیر وارد کنید:\n`/vip CODE`")
        return

    code = message.command[1].strip()
    result = use_vip_code(code, user_id)

    if result == "used":
        await message.reply("این کد قبلاً استفاده شده است.")
    elif result == "not_found":
        await message.reply("کد وارد شده نامعتبر است.")
    elif result == "success":
        await message.reply("پلن VIP با موفقیت برای شما فعال شد به مدت 15 روز با حجم روزانه 5 گیگ.")
    else:
        await message.reply("خطایی رخ داده است. لطفاً مجدداً تلاش کنید.")
