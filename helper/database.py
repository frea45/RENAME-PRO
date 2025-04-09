import pymongo
import os
from helper.date import add_date
from config import *
import time

mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]
dbcol = db["user"]
vipcol = db["vip_codes"]
#vip_codes_col = db["vip_codes"]
# Total User
def total_user():
    return dbcol.count_documents({})

# insert bot Data
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

# insert user data
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

def addthumb(chat_id, file_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": file_id}})

def delthumb(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": None}})

def addcaption(chat_id, caption):
    dbcol.update_one({"_id": chat_id}, {"$set": {"caption": caption}})

def delcaption(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"caption": None}})

def dateupdate(chat_id, date):
    dbcol.update_one({"_id": chat_id}, {"$set": {"date": date}})

def used_limit(chat_id, used):
    dbcol.update_one({"_id": chat_id}, {"$set": {"used_limit": used}})

def usertype(chat_id, type):
    dbcol.update_one({"_id": chat_id}, {"$set": {"usertype": type}})

def uploadlimit(chat_id, limit):
    dbcol.update_one({"_id": chat_id}, {"$set": {"uploadlimit": limit}})

def addpre(chat_id):
    date = add_date()
    dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": date[0]}})

def addpredata(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": None}})

def daily(chat_id, date):
    dbcol.update_one({"_id": chat_id}, {"$set": {"daily": date}})

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

# VIP code management
def add_vip_code(code: str):
    vipcol.insert_one({"code": code, "used": False})

def is_valid_vip_code(code: str):
    return vipcol.find_one({"code": code, "used": False})

def mark_vip_code_used(code: str):
    vipcol.update_one({"code": code}, {"$set": {"used": True}})

def update_user_plan(user_id: int, upload_limit: int, user_type: str, days: int):
    expire_date = int(time.time()) + days * 86400
    dbcol.update_one(
        {"_id": user_id},
        {"$set": {
            "uploadlimit": upload_limit,
            "usertype": user_type,
            "prexdate": expire_date
        }}
    )
"""
def use_vip_code(user_id: int, code: str):
    code_data = is_valid_vip_code(code)
    if not code_data:
        return False
    update_user_plan(user_id, 5368709120, "Vip", 15)
    mark_vip_code_used(code)
    return True
    """
def use_vip_code(code):
    vip_code = vip_codes_col.find_one({"code": code, "used": False})
    if vip_code:
        vip_codes_col.update_one({"code": code}, {"$set": {"used": True}})
        return True
    return False
