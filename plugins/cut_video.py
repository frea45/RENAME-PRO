import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import DOWNLOAD_LOCATION, LOG_CHANNEL
from helper.utils import humanbytes
from helper.ffmpeg import cut_video_ffmpeg

user_cut_data = {}

@Client.on_callback_query(filters.regex(r"cut_(.+)"))
async def ask_start_time(client, callback_query):
    file_id = callback_query.data.split("_", 1)[1]
    user_id = callback_query.from_user.id

    user_cut_data[user_id] = {"file_id": file_id}
    await callback_query.message.edit_text("زمان **شروع** ویدیو رو بفرست (مثلاً `00:00:10`):")

@Client.on_message(filters.private & filters.text)
async def handle_cut_times(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_cut_data:
        return

    cut_data = user_cut_data[user_id]
    if "start" not in cut_data:
        cut_data["start"] = message.text.strip()
        await message.reply_text("حالا زمان **پایان** ویدیو رو بفرست (مثلاً `00:01:00`):")
    else:
        cut_data["end"] = message.text.strip()
        file_id = cut_data["file_id"]
        start_time = cut_data["start"]
        end_time = cut_data["end"]

        await message.reply_text("در حال دانلود و برش ویدیو...")
        try:
            media_msg = await client.get_messages(message.chat.id, file_id)
            file_path = await media_msg.download(file_name=DOWNLOAD_LOCATION)
            cut_path = f"{file_path}_cut.mp4"

            await cut_video_ffmpeg(file_path, cut_path, start_time, end_time)

            await client.send_video(
                chat_id=LOG_CHANNEL,
                video=cut_path,
                caption=f"برش ویدیو توسط: [{message.from_user.first_name}](tg://user?id={user_id})"
            )

            await message.reply_video(
                video=cut_path,
                caption="ویدیوی برش‌خورده آماده‌ست!"
            )
        except Exception as e:
            await message.reply_text(f"خطا هنگام برش ویدیو:\n`{e}`")
        finally:
            if os.path.exists(file_path): os.remove(file_path)
            if os.path.exists(cut_path): os.remove(cut_path)
            user_cut_data.pop(user_id, None)
