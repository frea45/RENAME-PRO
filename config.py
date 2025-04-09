import os, re


BOT_TOKEN = os.environ.get("BOT_TOKEN", "1996499923:AAGVCjT4msY1AOHb-qtalwMsrwu0dD65k7g")
API_ID = int(os.environ.get("API_ID", "3335796"))
API_HASH = os.environ.get("API_HASH", "138b992a0e672e8346d8439c3f42ea78")
#OWNER = int(os.environ.get("OWNER", "763990585"))
BOT_USERNAME = os.environ.get('BOT_USERNAME', "ir_renamebot")

FORCE_SUBS = os.environ.get("FORCE_SUBS", "ir_botz")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001792962793"))

DB_URL = os.environ.get("DB_URL", "mongodb+srv://abirhasan2005:abirhasan@cluster0.i6qzp.mongodb.net/cluster0?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DB_NAME", "renamebot-premium")

STRING = os.environ.get("STRING", "")
BOT_PIC = os.environ.get("BOT_PIC", "https://telegra.ph/file/19eeb26fa2ce58765917a.jpg")


OWNER = [int(os.environ.get("OWNER", "763990585"))]



# if you need to add verify system then dm me on telegram

SHORTNER_URL = os.environ.get("SHORTNER_URL", "")
SHORTNER_API = os.environ.get("SHORTNER_API", "")
TOKEN_TIMEOUT = os.environ.get("TOKEN_TIMEOUT", "")
