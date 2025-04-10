from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import find_one, activate_gift_plan

@Client.on_message(filters.command("gift"))
async def gift_plan(client: Client, message: Message):
    user_id = message.from_user.id
    user_data = find_one(user_id)

    if not user_data:
        await message.reply("اول /start بزن تا ثبت‌نام بشی.")
        return

    current_plan = user_data.get("usertype", "Free")
    gift_used = user_data.get("gift_used", False)

    if current_plan in ["Silver", "Gold", "Diamond"]:
        await message.reply("شما در حال حاضر پلن ویژه دارید و نمی‌تونید پلن هدیه بگیرید.")
        return

    if gift_used:
        await message.reply("شما قبلاً از پلن هدیه استفاده کرده‌اید.")
        return

    # فعال‌سازی پلن هدیه
    activate_gift_plan(user_id)
    await message.reply("پلن هدیه ۷ روزه با حجم روزانه ۵ گیگ برات فعال شد. مبارک باشه!")
