import pymongo
import time
from datetime import datetime, timedelta
from helper.date import add_date
from config import DB_URL, DB_NAME

# اتصال به MongoDB
mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]
dbcol = db["user"]
vipcol = db["vip_codes"]

def total_user():
    return dbcol.count_documents({})

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

def find(chat_id):
    result = dbcol.find_one({"_id": chat_id})
    if result:
        return [result.get("file_id"), result.get("caption")]
    return [None, None]

def find_one(id):
    return dbcol.find_one({"_id": id})

def getid():
    return [key["_id"] for key in dbcol.find()]

def delete(id):
    dbcol.delete_one(id)

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
def total_rename(chat_id, renamed_file): dbcol.update_one({"_id": chat_id}, {"$set": {"total_rename": str(int(renamed_file) + 1)}})
def total_size(chat_id, total_size, now_file_size): dbcol.update_one({"_id": chat_id}, {"$set": {"total_size": str(int(total_size) + now_file_size)}})

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
    vipcol.update_one({"code": code}, {"$set": {"used": True, "used_by": user_id}})
    update_user_plan(
        user_id=user_id,
        usertype="VIP",
        daily_limit=5 * 1024 * 1024 * 1024,
        days=15
    )
    return "success"

def has_used_gift(user_id: int):
    user_data = dbcol.find_one({"_id": user_id})
    return user_data.get("gift_used", False)

def mark_gift_used(user_id: int):
    dbcol.update_one({"_id": user_id}, {"$set": {"gift_used": True}})

def is_gift_used(user_id: int) -> bool:
    user = dbcol.find_one({"_id": user_id})
    gift_plan = user.get("gift_plan", {})
    return gift_plan.get("used", False)

def activate_gift_plan(user_id: int):
    end_date = datetime.utcnow() + timedelta(days=7)
    gift_data = {
        "used": True,
        "daily_limit": 5 * 1024**3,  # 5 گیگ
        "end_date": end_date.timestamp()
    }
    dbcol.update_one(
        {"_id": user_id},
        {"$set": {"gift_plan": gift_data}},
        upsert=True
    )
