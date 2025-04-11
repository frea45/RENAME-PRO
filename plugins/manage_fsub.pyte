from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import OWNER
from helper.database import get_fsub_channels, add_fsub_channel, remove_fsub_channel

# نمایش منوی مدیریت کانال‌های اجباری
@Client.on_message(filters.command("add_fsub") & filters.user(OWNER))
async def add_fsub_menu(client, message):
    channels = get_fsub_channels()
    if not channels:
        txt = "هیچ کانالی اضافه نشده است."
    else:
        txt = "**کانال‌های اجباری:**\n\n"
        for ch in channels:
            txt += f"- {ch}\n"

    keyboard = [
        [InlineKeyboardButton("➕ افزودن کانال", callback_data="add_fsub_channel")]
    ]

    for ch in channels:
        keyboard.append(
            [InlineKeyboardButton(f"❌ حذف {ch}", callback_data=f"delconf|{ch}")]
        )

    await message.reply(
        txt,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# هندلر افزودن کانال جدید
@Client.on_callback_query(filters.regex(r"^add_fsub_channel$"))
async def ask_new_channel(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text("لطفا یوزرنیم کانال را با @ بفرستید:")
    return

# تأیید حذف یک کانال
@Client.on_callback_query(filters.regex(r"^delconf\|(.+)$"))
async def confirm_delete_channel(client, callback_query: CallbackQuery):
    channel = callback_query.data.split("|", 1)[1]
    keyboard = [
        [
            InlineKeyboardButton("بله", callback_data=f"delete_fsub|{channel}"),
            InlineKeyboardButton("لغو", callback_data="cancel_del")
        ]
    ]
    await callback_query.message.edit_text(
        f"آیا کانال {channel} حذف شود؟",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# لغو عملیات حذف و حذف پیام
@Client.on_callback_query(filters.regex(r"^cancel_del$"))
async def cancel_delete(client, callback_query: CallbackQuery):
    await callback_query.message.delete()

# حذف کانال و بازگشت به منو
@Client.on_callback_query(filters.regex(r"^delete_fsub\|(.+)$"))
async def delete_channel(client, callback_query: CallbackQuery):
    channel = callback_query.data.split("|", 1)[1]
    remove_fsub_channel(channel)
    await callback_query.answer("با موفقیت حذف شد.", show_alert=False)
    # بازگشت به منوی اصلی
    channels = get_fsub_channels()
    if not channels:
        txt = "هیچ کانالی اضافه نشده است."
    else:
        txt = "**کانال‌های اجباری:**\n\n"
        for ch in channels:
            txt += f"- {ch}\n"

    keyboard = [
        [InlineKeyboardButton("➕ افزودن کانال", callback_data="add_fsub_channel")]
    ]

    for ch in channels:
        keyboard.append(
            [InlineKeyboardButton(f"❌ حذف {ch}", callback_data=f"delconf|{ch}")]
        )

    await callback_query.message.edit_text(
        txt,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
