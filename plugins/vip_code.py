from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER
from helper.database import add_vip_code, use_vip_code, find_one
import random
import string

# ساخت کد VIP فقط توسط ادمین
@Client.on_message(filters.private & filters.command("crate_vip"))
async def create_vip_code(client, message: Message):
    if message.from_user.id != OWNER:
        return await message.reply("شما اجازه استفاده از این دستور را ندارید.")

    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    add_vip_code(code)
    await message.reply(f"کد VIP ساخته شد:\n\n`/vip {code}`", quote=True)

# استفاده از کد VIP توسط کاربران رایگان
@Client.on_message(filters.private & filters.command("vip"))
async def redeem_vip_code(client, message: Message):
    user_id = message.from_user.id
    user_data = find_one(user_id)

    if not user_data:
        return await message.reply("ابتدا /start را ارسال کنید.")

    if user_data.get("usertype") != "Free":
        return await message.reply("فقط کاربران با پلن رایگان می‌توانند از کد VIP استفاده کنند.")

    try:
        code = message.text.split(" ", 1)[1].strip()
    except IndexError:
        return await message.reply("لطفاً کد VIP را به صورت زیر وارد کنید:\n`/vip CODE`", quote=True)

    result = use_vip_code(code, user_id)
    if result == "used":
        return await message.reply("این کد قبلاً استفاده شده است.")
    elif result == "not_found":
        return await message.reply("کد وارد شده نامعتبر است.")
    elif result == "success":
        return await message.reply("پلن VIP با موفقیت برای شما فعال شد به مدت 15 روز با حجم روزانه 5 گیگ.")
