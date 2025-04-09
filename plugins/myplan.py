import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import find_one, used_limit, uploadlimit, usertype
from helper.database import daily as daily_
from helper.progress import humanbytes
from helper.date import check_expi
from datetime import datetime, date as date_

def progress_bar(used, total):
    percent = int((used / total) * 100) if total != 0 else 0
    filled = int(percent / 10)
    empty = 10 - filled
    bar = "▰" * filled + "▱" * empty
    return f"[{bar}] {percent}%"

@Client.on_message(filters.private & filters.command(["myplan"]))
async def show_plan(client, message):
    used_ = find_one(message.from_user.id)
    daily = used_["daily"]
    today = int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
    if daily != today:
        daily_(message.from_user.id, today)
        used_limit(message.from_user.id, 0)

    _newus = find_one(message.from_user.id)
    used = _newus["used_limit"]
    limit = _newus["uploadlimit"]
    remain = int(limit) - int(used)
    user = _newus["usertype"]
    ends = _newus["prexdate"]

    bar = progress_bar(used, limit)

    if ends and user != "Free":
        pre_check = check_expi(ends)
        if pre_check == False:
            uploadlimit(message.from_user.id, 1288490188)
            usertype(message.from_user.id, "Free")
            ends = None
            user = "Free"

    if ends:
        normal_date = datetime.fromtimestamp(ends).strftime('%Y-%m-%d')
        remaining_days = (datetime.fromtimestamp(ends) - datetime.now()).days
        text = f"""**🔺 نام کاربر :** {message.from_user.mention}
**🔺 آیدی عددی شما :** `{message.from_user.id}`
🔮 **پلن فعلی شما :** {user} 
💽 **حجم محدودیت روزانه :** {humanbytes(limit)} 
✅ **حجم استفاده شده :** {humanbytes(used)} 
☑️ **حجم باقی مانده :** {humanbytes(remain)} 
📊 **درصد استفاده شده :** {bar}
⌚ **فاصله زمانی بین فایل ها :** ندارد
📆 **تاریخ اتمام پلن :** {normal_date}
⏳ **روزهای باقی‌مانده :** {remaining_days} روز"""
    else:
        text = f"""**🔺 نام کاربر :** {message.from_user.mention}
**🔺 آیدی عددی شما :** `{message.from_user.id}`
🔮 **پلن فعلی شما :** {user} 
💽 **حجم محدودیت روزانه :** {humanbytes(limit)} 
✅ **حجم استفاده شده :** {humanbytes(used)} 
☑️ **حجم باقی مانده :** {humanbytes(remain)} 
📊 **درصد استفاده شده :** {bar}
⌚ **فاصله زمانی بین فایل ها :** 60 ثانیه"""

    if user == "Free":
        await message.reply(text, quote=True, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔖 ارتقا پلن", callback_data="upgrade"),
             InlineKeyboardButton("✖️ بستن", callback_data="cancel")]
        ]))
    else:
        await message.reply(text, quote=True, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✖️ بستن ✖️", callback_data="cancel")]
        ]))
