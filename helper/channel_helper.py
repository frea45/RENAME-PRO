import json
import os

CHANNEL_FILE = "channels.json"

def load_channels():
    """
    خواندن لیست کانال‌ها از فایل channels.json
    خروجی: لیست کانال‌ها
    """
    if not os.path.exists(CHANNEL_FILE):
        return []
    try:
        with open(CHANNEL_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_channels(channels: list):
    """
    ذخیره‌سازی لیست کانال‌ها در فایل channels.json
    ورودی: لیست کانال‌ها
    """
    with open(CHANNEL_FILE, "w") as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
