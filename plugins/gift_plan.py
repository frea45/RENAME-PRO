from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import activate_gift_plan_db, find_one

@Client.on_message(filters.command("gift"))
async def activate_gift_plan(client, message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    if user_data.get("plan") in ["silver", "gold", "diamond"]:
        return await message.reply("شما قبلاً یک پلن فعال دارید و نمی‌توانید از پلن هدیه استفاده کنید.")

    if user_data.get("gift_used"):
        return await message.reply("شما قبلاً از پلن هدیه استفاده کرده‌اید.")

    # فعال‌سازی پلن هدیه
    activate_gift_plan_db(user_id)

    # ثبت استفاده از هدیه
    from helper.database import set_gift_used
    set_gift_used(user_id)

    await message.reply("پلن هدیه 7 روزه با موفقیت فعال شد!\nحجم روزانه: 5 گیگ")

    # ارسال گزارش به کانال لاگ
    log_channel = -100123456789  # شناسه کانال لاگ واقعی رو بذار
    user = message.from_user
    text = f"""پلن هدیه فعال شد.
نام کاربر: {user.first_name}
آیدی عددی: {user.id}
نام پلن: gift"""
    try:
        await client.send_message(log_channel, text)
    except:
        pass
