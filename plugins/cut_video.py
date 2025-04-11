from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import sleep
import os
import subprocess

user_cut_sessions = {}

@Client.on_callback_query(filters.regex("cut_video"))
async def ask_start_time(client, callback_query: CallbackQuery):
    message = callback_query.message
    file = message.video or message.document

    if not file or not file.file_name.endswith((".mp4", ".mkv", ".mov", ".avi")):
        await callback_query.answer("این فایل قابل برش نیست.", show_alert=True)
        return

    user_cut_sessions[callback_query.from_user.id] = {
        "file_id": file.file_id,
        "file_name": file.file_name,
        "chat_id": message.chat.id,
        "message_id": message.id
    }
    await callback_query.message.reply_text("⏱ لطفاً زمان **شروع برش** را وارد کنید (مثلاً 00:01:30):")
    await callback_query.answer()

@Client.on_message(filters.private & filters.text)
async def receive_cut_times(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_cut_sessions:
        return

    session = user_cut_sessions[user_id]
    if "start_time" not in session:
        session["start_time"] = message.text.strip()
        await message.reply("⏱ حالا زمان **پایان برش** را وارد کنید (مثلاً 00:03:00):")
        return

    session["end_time"] = message.text.strip()
    await message.reply("✂️ در حال برش فایل، لطفاً صبر کنید...")

    file_path = await client.download_media(session["file_id"])
    out_path = f"cut_{session['file_name']}"

    cmd = [
        "ffmpeg", "-i", file_path,
        "-ss", session["start_time"],
        "-to", session["end_time"],
        "-c", "copy", out_path
    ]
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if os.path.exists(out_path):
        await client.send_document(session["chat_id"], out_path, caption="✅ ویدیو برش داده شد.")
        os.remove(out_path)
    else:
        await message.reply("❌ مشکلی در برش فایل به‌وجود آمد.")

    os.remove(file_path)
    user_cut_sessions.pop(user_id)
