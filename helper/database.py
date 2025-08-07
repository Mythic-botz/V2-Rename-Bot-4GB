import pymongo
import os
from helper.date import add_date
from config import *
mongo = pymongo.MongoClient(DATABASE_URL)
db = mongo[DATABASE_NAME]
dbcol = db["user"]



# Total User
def total_user():
    user = dbcol.count_documents({})
    return user


# Insert Bot Data
def botdata(chat_id):
    bot_id = int(chat_id)
    try:
        bot_data = {"_id": bot_id, "total_rename": 0, "total_size": 0}
        dbcol.insert_one(bot_data)
    except:
        pass


# Total Renamed Files
def total_rename(chat_id, renamed_file):
    now = int(renamed_file) + 1
    dbcol.update_one({"_id": chat_id}, {"$set": {"total_rename": str(now)}})


# Total Renamed File Size
def total_size(chat_id, total_size, now_file_size):
    now = int(total_size) + now_file_size
    dbcol.update_one({"_id": chat_id}, {"$set": {"total_size": str(now)}})


# Insert User Data
def insert(chat_id):
    user_id = int(chat_id)
    
    # Check if user already exists
    existing_user = find_one(user_id)
    if existing_user:
        # Update existing user with missing fields
        missing_fields = {}
        
        if "date" not in existing_user:
            missing_fields["date"] = 0
        if "daily" not in existing_user:
            missing_fields["daily"] = 0
        if "uploadlimit" not in existing_user:
            missing_fields["uploadlimit"] = 5368709120
        if "used_limit" not in existing_user:
            missing_fields["used_limit"] = 0
        if "usertype" not in existing_user:
            missing_fields["usertype"] = "Free"
        if "prexdate" not in existing_user:
            missing_fields["prexdate"] = None
        if "metadata" not in existing_user:
            missing_fields["metadata"] = False
        if "metadata_code" not in existing_user:
            missing_fields["metadata_code"] = "By @Madflix_Bots"
        if "file_id" not in existing_user:
            missing_fields["file_id"] = None
        if "caption" not in existing_user:
            missing_fields["caption"] = None
            
        if missing_fields:
            dbcol.update_one({"_id": user_id}, {"$set": missing_fields})
        
        return True
    
    # Create new user with all fields
    user_det = {
        "_id": user_id, 
        "file_id": None, 
        "caption": None, 
        "daily": 0, 
        "date": 0,
        "uploadlimit": 5368709120, 
        "used_limit": 0, 
        "usertype": "Free", 
        "prexdate": None,
        "metadata": False, 
        "metadata_code": "By @Madflix_Bots"
    }
    try:
        dbcol.insert_one(user_det)
        return True
    except:
        return True


# Add Thumbnail Data
def addthumb(chat_id, file_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": file_id}})

def delthumb(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": None}})




# ============= Metadata Function Code =============== #

def setmeta(chat_id, bool_meta):
    dbcol.update_one({"_id": chat_id}, {"$set": {"metadata": bool_meta}})

def setmetacode(chat_id, metadata_code):
    dbcol.update_one({"_id": chat_id}, {"$set": {"metadata_code": metadata_code}})

# ============= Metadata Function Code =============== #



# Add Caption Data
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


# Add Premium Data
def addpre(chat_id):
    date = add_date()
    dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": date[0]}})

def addpredata(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": None}})

def daily(chat_id, date):
    dbcol.update_one({"_id": chat_id}, {"$set": {"daily": date}})

def find(chat_id):
    id = {"_id": chat_id}
    x = dbcol.find(id)
    for i in x:
        file = i.get("file_id")
        caption = i.get("caption")
        metadata = i.get("metadata", False)
        metadata_code = i.get("metadata_code", "By @Madflix_Bots")
        return [file, caption, metadata, metadata_code]

def getid():
    values = []
    for key in dbcol.find():
        id = key["_id"]
        values.append((id))
    return values

def delete(id):
    dbcol.delete_one(id)

def find_one(id):
    user = dbcol.find_one({"_id": id})
    if user:
        # Ensure all required fields exist with default values
        defaults = {
            "file_id": None,
            "caption": None,
            "daily": 0,
            "date": 0,
            "uploadlimit": 5368709120,
            "used_limit": 0,
            "usertype": "Free",
            "prexdate": None,
            "metadata": False,
            "metadata_code": "By @Madflix_Bots"
        }
        
        # Add missing fields
        for key, default_value in defaults.items():
            if key not in user:
                user[key] = default_value
                
        return user
    return None



    

# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Back-Up Channel @JishuBotz
# Developer @JishuDeveloper & @MadflixOfficial