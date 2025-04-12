from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import OWNER, FORCE_SUBS
from helper.channel_helper import save_channels, load_channels

channel_data = {}

@Client.on_message(filters.command("manger_sub") & filters.user(ADMINS))
async def manage_sub_handler(client, message: Message):
    user_id = message.from_user.id
    channels = load_channels()

    # اطمینان از وجود FORCE_SUBS
    if FORCE_SUBS and (FORCE_SUBS not in channels):
        channels.insert(0, FORCE_SUBS if FORCE_SUBS.startswith("@") else "@" + FORCE_SUBS)
        save_channels(channels)

    buttons = [[InlineKeyboardButton(ch, callback_data=f"select_channel|{ch}")] for ch in channels]
    buttons.append([InlineKeyboardButton("➕ افزودن کانال", callback_data="add_channel")])

    sent = await message.reply("**تنظیمات کانال :**", reply_markup=InlineKeyboardMarkup(buttons))
    channel_data[user_id] = {
        "msg_id": sent.id,
        "chat_id": sent.chat.id,
        "channels": channels
    }


@Client.on_callback_query(filters.regex("add_channel"))
async def ask_username(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await callback_query.message.reply("یوزرنیم کانال خود را ارسال کنید:")
    await callback_query.answer()


@Client.on_message(filters.text & filters.user(ADMINS))
async def handle_channel_username(client, message: Message):
    user_id = message.from_user.id
    if user_id not in channel_data:
        return

    username = message.text.strip()
    if not username.startswith("@"):
        await message.reply("لطفاً یوزرنیم را با @ وارد کنید.")
        return

    if username in channel_data[user_id]["channels"]:
        await message.reply("این کانال قبلاً افزوده شده است.")
        return

    # افزودن کانال
    channel_data[user_id]["channels"].append(username)
    save_channels(channel_data[user_id]["channels"])

    # بروزرسانی پیام اصلی
    buttons = [
        [InlineKeyboardButton(ch, callback_data=f"select_channel|{ch}")]
        for ch in channel_data[user_id]["channels"]
    ]
    buttons.append([InlineKeyboardButton("➕ افزودن کانال", callback_data="add_channel")])

    await client.edit_message_reply_markup(
        chat_id=channel_data[user_id]["chat_id"],
        message_id=channel_data[user_id]["msg_id"],
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex(r"select_channel\|(.+)"))
async def ask_remove_channel(client, callback_query: CallbackQuery):
    ch = callback_query.data.split("|")[1]
    user_id = callback_query.from_user.id
    await callback_query.message.reply(
        f"کانال {ch} انتخاب شده است.\nآیا می‌خواهید آن را حذف کنید؟",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بله", callback_data=f"delete_channel|{ch}"),
             InlineKeyboardButton("نه", callback_data="cancel_delete")]
        ])
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r"delete_channel\|(.+)"))
async def delete_channel(client, callback_query: CallbackQuery):
    ch = callback_query.data.split("|")[1]
    user_id = callback_query.from_user.id

    if user_id not in channel_data or ch not in channel_data[user_id]["channels"]:
        await callback_query.answer("کانال یافت نشد!", show_alert=True)
        return

    channel_data[user_id]["channels"].remove(ch)
    save_channels(channel_data[user_id]["channels"])

    # بروزرسانی پیام اصلی
    buttons = [
        [InlineKeyboardButton(ch, callback_data=f"select_channel|{ch}")]
        for ch in channel_data[user_id]["channels"]
    ]
    buttons.append([InlineKeyboardButton("➕ افزودن کانال", callback_data="add_channel")])

    await client.edit_message_reply_markup(
        chat_id=channel_data[user_id]["chat_id"],
        message_id=channel_data[user_id]["msg_id"],
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    await callback_query.message.delete()
    await callback_query.answer("کانال حذف شد.", show_alert=False)


@Client.on_callback_query(filters.regex("cancel_delete"))
async def cancel_delete(client, callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer("تغییری ایجاد نشد", show_alert=False)
