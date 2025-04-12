from datetime import date as date_
import datetime
import os, re
import asyncio
import random
from script import *
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import time
from pyrogram import Client, filters, enums
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
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
    txt=f"""**👋 سلام {message.from_user.mention} |🥰😉 \n\n• به ربات تغییرنام فایل ها خوش آمدید ❤️\n\n• هم اکنون یک فایل برایم ارسال کنید تا من\nنام آن را به دلخواه شما تغییر دهم.😊\n\n🖍️ سازنده ربات : [FﾑRSみɨの-BﾑŊの](t.me/farshidband)**"""
#    await message.react(emoji="🔥")
    await message.reply_photo(photo=BOT_PIC,
                                caption=txt,
                                reply_markup=InlineKeyboardMarkup(
                                        [
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
            await client.send_message(log_channel,f"<b><u>✅ کاربر جدیدی به ربات پیوست 😍</u></b> \n\n<b>🔺 آیدی عددی کاربر</b> : `{user_id}` \n<b>🔺 نام کاربر </b> : {message.from_user.first_name} \n<b>🔺فامیلی کاربر</b> : {message.from_user.last_name} \n<b>🔺یوزرنیم </b> : @{message.from_user.username} \n<b>User Mention</b> : {message.from_user.mention} \n<b>🔺لینک کاربر</b> : <a href='tg://openmessage?user_id={user_id}'>Click Here</a> \n<b>✔️ پلن کاربر</b> : {user}",
                                                                                                       reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔺  Rᴇsᴛʀɪᴄᴛ Usᴇʀ ( **PM** )  🔺", callback_data="ceasepower")]]))
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
    else:
        # Forward a single message
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
            pattern = '%Y-%m-%d'
            epcho = int(time.mktime(time.strptime(str(today), pattern)))
            daily_(message.from_user.id, epcho)
            used_limit(message.from_user.id, 0)
        remain = limit - used
        if remain < int(file.file_size):
            await message.reply_text(f"**🚫متاسفانه سهمیه مصرف روزانه شما تمام شده است!😔\n\n🔋حجم فایل شناسایی شده: <u>{humanbytes(file.file_size)}</u>\n📬 میزان حجم استفاده شده:<u>{humanbytes(used)}</u>\n\n🚧 فقط <u>{humanbytes(remain)}</u> از مصرف روزانه تان باقی مانده است.\n\nاگر می خواهید نام فایل های پرحجم را تغییر دهید پلن خود را ارتقا دهید.\n🔚 جهت ارتقا پلن ⬅️ /upgrade **", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔖 ارتقای پلن ", callback_data="upgrade")]]))
            return
        if value < file.file_size:
            
            if STRING:
                if buy_date == None:
                    await message.reply_text(f"**ربات قادر به آپلود فایل بالای 2GB نیست!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔖 ارتقای پلن", callback_data="upgrade")]]))
                    return
                pre_check = check_expi(buy_date)
                if pre_check == True:
                    await message.reply_text(f"""__**✅ عالی ، حالا برای شروع کلیک کن.**__\n\n**📁 نام فعلی فایل :**\n✔️ :- `{filename}`\n**🔮 حجم فایل :- {humanize.naturalsize(file.file_size)} **\n**DC ID** :- {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✍️ تغییرنام فایل", callback_data="rename"), InlineKeyboardButton("✖️ لغو", callback_data="cancel")]]))
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
            fileid = file.file_id
            total_rename(int(botid), prrename)
            total_size(int(botid), prsize, file.file_size)
            await message.reply_text(f"""__✅ عالی ، حالا برای شروع کلیک کن.__\n\n**📁 نام فعلی فایل :**\n • :- `{filename}`\n**🔮 حجم فایل ** :- {filesize}\n**DC ID** :- {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖️ لغو", callback_data="cancel"),
                  InlineKeyboardButton("✍️ تغییرنام فایل", callback_data="rename")]]))
              
              
              
