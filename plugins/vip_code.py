import random
import string
from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER
from helper.database import add_vip_code, use_vip_code, update_user_plan

# تولید کد VIP یکبار مصرف توسط ادمین
@Client.on_message(filters.private & filters.command("crate_vip"))
async def create_vip_code(client: Client, message: Message):
    if message.from_user.id not in OWNER:
        return await message.reply("شما اجازه استفاده از این دستور را ندارید.")
    
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    add_vip_code(code)
    await message.reply(f"کد VIP با موفقیت ساخته شد:\n\n`{code}`\n\nاین کد فقط یک‌بار قابل استفاده است.")

# فعالسازی پلن VIP توسط کاربر
@Client.on_message(filters.private & filters.command("vip"))
async def use_vip(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("لطفاً کد VIP را به صورت صحیح وارد کنید.\n\nمثال:\n`/vip ABCD1234`")
    
    code = message.command[1]
    used = use_vip_code(code)
    if not used:
        return await message.reply("کد نامعتبر یا قبلاً استفاده شده است.")

    update_user_plan(message.from_user.id, plan_type="VIP", days=15, daily_limit=5 * 1024**3)
    await message.reply("پلن VIP با موفقیت فعال شد!\nمدت: 15 روز\nحجم روزانه: 5 گیگابایت\nبدون محدودیت حجم فایل.")
