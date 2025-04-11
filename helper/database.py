import pymongo
import os
import time
from helper.date import add_date
from config import *
from datetime import datetime, timedelta

mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]
dbcol = db["user"]
vipcol = db["vip_codes"]

# Total User
def total_user():
    return dbcol.count_documents({})

# Insert bot Data
def botdata(chat_id):
    try:
        dbcol.insert_one({"_id": int(chat_id), "total_rename": 0, "total_size": 0})
    except:
        pass

def total_rename(chat_id, renamed_file):
    now = int(renamed_file) + 1
    dbcol.update_one({"_id": chat_id}, {"$set": {"total_rename": str(now)}})

def total_size(chat_id, total_size, now_file_size):
    now = int(total_size) + now_file_size
    dbcol.update_one({"_id": chat_id}, {"$set": {"total_size": str(now)}})

# Insert user data
def insert(chat_id):
    try:
        dbcol.insert_one({
            "_id": int(chat_id),
            "file_id": None,
            "caption": None,
            "daily": 0,
            "date": 0,
            "uploadlimit": 1074490188,
            "used_limit": 0,
            "usertype": "Free",
            "prexdate": None
        })
    except:
        return True

# Various setters
def addthumb(chat_id, file_id): dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": file_id}})
def delthumb(chat_id): dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": None}})
def addcaption(chat_id, caption): dbcol.update_one({"_id": chat_id}, {"$set": {"caption": caption}})
def delcaption(chat_id): dbcol.update_one({"_id": chat_id}, {"$set": {"caption": None}})
def dateupdate(chat_id, date): dbcol.update_one({"_id": chat_id}, {"$set": {"date": date}})
def used_limit(chat_id, used): dbcol.update_one({"_id": chat_id}, {"$set": {"used_limit": used}})
def usertype(chat_id, type): dbcol.update_one({"_id": chat_id}, {"$set": {"usertype": type}})
def uploadlimit(chat_id, limit): dbcol.update_one({"_id": chat_id}, {"$set": {"uploadlimit": limit}})
def addpre(chat_id): dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": add_date()[0]}})
def addpredata(chat_id): dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": None}})
def daily(chat_id, date): dbcol.update_one({"_id": chat_id}, {"$set": {"daily": date}})

# User utilities
def find(chat_id):
    result = dbcol.find_one({"_id": chat_id})
    if result:
        return [result.get("file_id"), result.get("caption")]
    return [None, None]

def getid():
    return [key["_id"] for key in dbcol.find()]

def delete(id):
    dbcol.delete_one(id)

def find_one(id):
    return dbcol.find_one({"_id": id})
    #--

# VIP code management
def add_vip_code(code: str):
    vipcol.insert_one({"code": code, "used": False})

def is_valid_vip_code(code: str):
    return vipcol.find_one({"code": code, "used": False})

def mark_vip_code_used(code: str):
    vipcol.update_one({"code": code}, {"$set": {"used": True}})

def update_user_plan(user_id: int, usertype: str = "Free", daily_limit: int = 1074490188, days: int = 0):
    expire_date = int(time.time()) + days * 86400 if days > 0 else None
    update_fields = {
        "usertype": usertype,
        "uploadlimit": daily_limit
    }
    if expire_date:
        update_fields["prexdate"] = expire_date

    dbcol.update_one({"_id": user_id}, {"$set": update_fields})

def use_vip_code(code: str, user_id: int):
    code_data = vipcol.find_one({"code": code})
    if not code_data:
        return "not_found"
    if code_data.get("used"):
        return "used"

    # بروزرسانی وضعیت کد
    vipcol.update_one({"code": code}, {"$set": {"used": True, "used_by": user_id}})

    # فعالسازی پلن VIP برای کاربر
    update_user_plan(
        user_id=user_id,
        usertype="VIP",
        daily_limit=5 * 1024 * 1024 * 1024,  # 5 گیگ
        days=15
    )
    return "success"

    update_user_plan2(
        user_id=user_id,
        usertype="7days",
        daily_limit=5 * 1024 * 1024 * 1024,  # 5 گیگ
        days=7
    )
    return "success"

"""
fsub_channels = []

def add_fsub_channel(username: str):
    if username not in fsub_channels:
        fsub_channels.append(username)

def remove_fsub_channel(username: str):
    if username in fsub_channels:
        fsub_channels.remove(username)

def get_fsub_channels():
    return fsub_channels
    """
def update_user_plan2(user_id: int, usertype: str = "Free", daily_limit: int = 1074490188, days: int = 0):
    expire_date = int(time.time()) + days * 86400 if days > 0 else None
    update_fields = {
        "usertype": usertype,
        "uploadlimit": daily_limit
    }
    if expire_date:
        update_fields["prexdate"] = expire_date

    result = dbcol.update_one({"_id": user_id}, {"$set": update_fields})
    return "success" if result.modified_count else "failed"

                          
