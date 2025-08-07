import os
import pymongo
from config import *
from helper.date import add_date

# 🌐 Connect to MongoDB using Render environment variable
mongo = pymongo.MongoClient(DATABASE_URL)
db = mongo[DATABASE_NAME]
dbcol = db["user"]

# 🧮 Total User Count
def total_user():
    return dbcol.count_documents({})

# 📝 Insert Bot Stats
def botdata(chat_id):
    try:
        dbcol.insert_one({"_id": int(chat_id), "total_rename": 0, "total_size": 0})
    except pymongo.errors.DuplicateKeyError:
        pass

# 📁 Track Rename Count
def total_rename(chat_id, renamed_file):
    now = int(renamed_file) + 1
    dbcol.update_one({"_id": chat_id}, {"$set": {"total_rename": str(now)}})

# 📦 Track Total Size Renamed
def total_size(chat_id, total_size, now_file_size):
    now = int(total_size) + now_file_size
    dbcol.update_one({"_id": chat_id}, {"$set": {"total_size": str(now)}})

# 👤 Insert New User
def insert(chat_id):
    user_det = {
        "_id": int(chat_id),
        "file_id": None,
        "caption": None,
        "daily": 0,
        "date": 0,
        "uploadlimit": 5368709120,  # 5GB
        "used_limit": 0,
        "usertype": "Free",
        "prexdate": None,
        "metadata": False,
        "metadata_code": "By @Madflix_Bots"
    }
    try:
        dbcol.insert_one(user_det)
    except pymongo.errors.DuplicateKeyError:
        return True

# 🖼️ Thumbnail Handling
def addthumb(chat_id, file_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": file_id}})

def delthumb(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": None}})

# 🏷️ Caption Handling
def addcaption(chat_id, caption):
    dbcol.update_one({"_id": chat_id}, {"$set": {"caption": caption}})

def delcaption(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"caption": None}})

# 🧠 Metadata Feature
def setmeta(chat_id, bool_meta):
    dbcol.update_one({"_id": chat_id}, {"$set": {"metadata": bool_meta}})

def setmetacode(chat_id, metadata_code):
    dbcol.update_one({"_id": chat_id}, {"$set": {"metadata_code": metadata_code}})

# 🔁 Daily & Limits
def dateupdate(chat_id, date):
    dbcol.update_one({"_id": chat_id}, {"$set": {"date": date}})

def used_limit(chat_id, used):
    dbcol.update_one({"_id": chat_id}, {"$set": {"used_limit": used}})

def usertype(chat_id, type):
    dbcol.update_one({"_id": chat_id}, {"$set": {"usertype": type}})

def uploadlimit(chat_id, limit):
    dbcol.update_one({"_id": chat_id}, {"$set": {"uploadlimit": limit}})

# ⭐ Premium Users
def addpre(chat_id):
    date = add_date()
    dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": date[0]}})

def addpredata(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": None}})

def daily(chat_id, date):
    dbcol.update_one({"_id": chat_id}, {"$set": {"daily": date}})

# 🔎 Fetch User Data
def find(chat_id):
    data = dbcol.find_one({"_id": chat_id})
    if not data:
        return [None, None, False, None]
    return [
        data.get("file_id"),
        data.get("caption"),
        data.get("metadata", False),
        data.get("metadata_code")
    ]

# 📄 Get All IDs
def getid():
    return [doc["_id"] for doc in dbcol.find()]

# ❌ Delete User
def delete(id):
    dbcol.delete_one({"_id": id})

# 🔍 Find One
def find_one(id):
    return dbcol.find_one({"_id": id})

# Jishu Developer 🚀
# Don’t Remove Credit 🥺
# @Madflix_Bots | @JishuBotz | Dev: @JishuDeveloper @MadflixOfficials