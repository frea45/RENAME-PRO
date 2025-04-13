
from datetime import date as date_
import datetime
import os, re
import asyncio
import random
from script import *
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import time
from pyrogram import Client, filters, enums
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery)
import humanize
from helper.progress import humanbytes
from helper.database import botdata, find_one, total_user
from helper.database import insert, find_one, used_limit, usertype, uploadlimit, addpredata, total_rename, total_size
from pyrogram.file_id import FileId
from helper.database import daily as daily_
from helper.date import check_expi
from config import *

bot_username = BOT_USERNAME
log_channel = LOG_CHANNEL
token = BOT_TOKEN
botid = token.split(':')[0]

user_cut_info = {}

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user_id = message.chat.id
    old = insert(int(user_id))
    try:
        id = message.text.split(' ')[1]
    except IndexError:
        id = None
    loading_sticker_message = await message.reply_sticker("CAACAgUAAxkBAAEKVaxlCWGs1Ri6ti45xliLiUeweCnu4AACBAADwSQxMYnlHW4Ls8gQMAQ")
    await asyncio.sleep(1)
    await loading_sticker_message.delete()
    txt=f"""**👋 سلام {message.from_user.mention} |🥰😉 

• به ربات تغییرنام فایل ها خوش آمدید ❤️

• هم اکنون یک فایل برایم ارسال کنید تا من
نام آن را به دلخواه شما تغییر دهم.😊

🖍️ سازنده ربات : [FﾑRSみɨの-BﾑŊの](t.me/farshidband)**"""
    await message.reply_photo(photo=BOT_PIC,
        caption=txt,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("کانال پشتیبانی", url="https://t.me/ir_botz")],
            [InlineKeyboardButton("📚 راهنمای ربات", callback_data='help'),
             InlineKeyboardButton("🏷️ ارتقا پلن", callback_data='upgrade')]
        ]))
    return

@Client.on_message((filters.private & (filters.document | filters.audio | filters.video)) | filters.channel & (filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    update_channel = FORCE_SUBS
    user_id = message.from_user.id
    if update_channel:
        try:
            await client.get_chat_member(update_channel, user_id)
        except UserNotParticipant:
            _newus = find_one(message.from_user.id)
            user = _newus["usertype"]
            await message.reply_text("<b>• برای کارکردن ربات در کانال زیر عضو شوید.\n\n🔚 سپس /start را کلیک کنید.😊👇👇</b>",
                reply_to_message_id=message.id,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("✅ عضویت ⚡ ", url=f"https://t.me/{update_channel}")]]))
            return
    botdata(int(botid))
    bot_data = find_one(int(botid))
    prrename = bot_data['total_rename']
    prsize = bot_data['total_size']
    user_deta = find_one(user_id)
    used_date = user_deta["date"]
    buy_date = user_deta["prexdate"]
    daily = user_deta["daily"]
    user_type = user_deta["usertype"]
    c_time = time.time()
    if user_type == "Free":
        LIMIT = 60
    else:
        LIMIT = 10
    then = used_date + LIMIT
    left = round(then - c_time)
    conversion = datetime.timedelta(seconds=left)
    ltime = str(conversion)
    if left > 0:
        await message.reply_text(f"**⚠️ بعد از گذشت تایم {ltime} ثانیه \nبعد فایل خود را ارسال کنید .😊**", reply_to_message_id=message.id)
        return
    media = await client.get_messages(message.chat.id, message.id)
    file = media.document or media.video or media.audio
    dcid = FileId.decode(file.file_id).dc_id
    filename = file.file_name
    file_id = file.file_id
    value = 1288490188
    used_ = find_one(message.from_user.id)
    used = used_["used_limit"]
    limit = used_["uploadlimit"]
    expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
    if expi != 0:
        today = date_.today()
        epcho = int(time.mktime(time.strptime(str(today), '%Y-%m-%d')))
        daily_(message.from_user.id, epcho)
        used_limit(message.from_user.id, 0)
    remain = limit - used
    if remain < int(file.file_size):
        await message.reply_text(f"**🚫متاسفانه سهمیه مصرف روزانه شما تمام شده است!😔\n\n🔋حجم فایل شناسایی شده: <u>{humanbytes(file.file_size)}</u>\n📬 میزان حجم استفاده شده:<u>{humanbytes(used)}</u>\n\n🚧 فقط <u>{humanbytes(remain)}</u> از مصرف روزانه تان باقی مانده است.\n\nاگر می خواهید نام فایل های پرحجم را تغییر دهید پلن خود را ارتقا دهید.\n🔚 جهت ارتقا پلن ⬅️ /upgrade **",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔖 ارتقای پلن ", callback_data="upgrade")]]))
        return
    if value < file.file_size:
        if STRING:
            if buy_date == None:
                await message.reply_text(f"**ربات قادر به آپلود فایل بالای 2GB نیست!**",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔖 ارتقای پلن", callback_data="upgrade")]]))
                return
            pre_check = check_expi(buy_date)
            if pre_check == True:
                await message.reply_text(
                    f"""__**✅ عالی ، حالا برای شروع کلیک کن.**__\n\n**📁 نام فعلی فایل :**\n✔️ :- `{filename}`\n**🔮 حجم فایل :- {humanize.naturalsize(file.file_size)} **\n**DC ID** :- {dcid}""",
                    reply_to_message_id=message.id,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("✖️ لغو", callback_data="cancel"),
                         InlineKeyboardButton("✍️ تغییرنام فایل", callback_data="rename")],
                        [InlineKeyboardButton("✂️ برش ویدیو", callback_data=f"cutvideo|{file_id}")]
                    ]))
                total_rename(int(botid), prrename)
                total_size(int(botid), prsize, file.file_size)
            else:
                uploadlimit(message.from_user.id, 1288490188)
                usertype(message.from_user.id, "Free")
                await message.reply_text(f'♨️مدت استفاده پلن شما به پایان رسید. \n {buy_date}', quote=True)
                return
        else:
            await message.reply_text("**ربات قادر به آپلود فایل بالای 2GB نیست!**")
            return
    else:
        if buy_date:
            pre_check = check_expi(buy_date)
            if pre_check == False:
                uploadlimit(message.from_user.id, 1288490188)
                usertype(message.from_user.id, "Free")
        filesize = humanize.naturalsize(file.file_size)
        total_rename(int(botid), prrename)
        total_size(int(botid), prsize, file.file_size)
        await message.reply_text(
            f"""__✅ عالی ، حالا برای شروع کلیک کن.__\n\n**📁 نام فعلی فایل :**\n • :- `{filename}`\n**🔮 حجم فایل ** :- {filesize}\n**DC ID** :- {dcid}""",
            reply_to_message_id=message.id,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✖️ لغو", callback_data="cancel"),
                 InlineKeyboardButton("✍️ تغییرنام فایل", callback_data="rename")],
                [InlineKeyboardButton("✂️ برش ویدیو", callback_data=f"cutvideo|{file_id}")]
            ]))

@Client.on_callback_query(filters.regex(r"^cutvideo\|"))
async def cutvideo_handler(client, callback_query: CallbackQuery):
    file_id = callback_query.data.split("|")[1]
    user_id = callback_query.from_user.id
    user_cut_info[user_id] = {"file_id": file_id}
    await callback_query.message.edit_text(
        "⏱ زمان شروع برش را وارد کنید:\n\nبه فرمت `00:01:30` (ساعت:دقیقه:ثانیه)",
        parse_mode="html")

@Client.on_message(filters.private & filters.text)
async def get_cut_times(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_cut_info:
        return
    info = user_cut_info[user_id]
    if "start" not in info:
        user_cut_info[user_id]["start"] = message.text.strip()
        await message.reply_text("⏱ حالا زمان پایان برش را وارد کنید:\n\nبه فرمت `00:02:45`")
        return
    user_cut_info[user_id]["end"] = message.text.strip()
    start = user_cut_info[user_id]["start"]
    end = user_cut_info[user_id]["end"]
    file_id = user_cut_info[user_id]["file_id"]
    del user_cut_info[user_id]
    status = await message.reply_text("⬇️ در حال دانلود فایل...")
    video_path = await client.download_media(file_id)
    output_path = f"cut_{os.path.basename(video_path)}"
    await status.edit_text("✂️ در حال برش ویدیو...")
    ffmpeg_cmd = f'ffmpeg -i "{video_path}" -ss {start} -to {end} -c copy "{output_path}" -y'
    process = await asyncio.create_subprocess_shell(ffmpeg_cmd)
    await process.communicate()
    await status.edit_text("⬆️ در حال ارسال فایل بریده‌شده...")
    await client.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_VIDEO)
    await message.reply_video(video=output_path, caption="✅ فایل بریده‌شده با موفقیت آماده شد.")
    os.remove(video_path)
    os.remove(output_path)
