from os import getenv
from sys import exit
from dotenv import load_dotenv
from time import time
from pyrogram import Client
import sqlite3
from .utils.logger import get_logger

start_time = time()
log = get_logger("bot")

load_dotenv("data.env", override=True)

# token = getenv("BOT_TOKEN", None)
session_string = getenv("SESSION_STRING")
# database_url = getenv("DATABASE_URL") 
# api_id = getenv("API_ID", None)
# api_hash = getenv("API_HASH", None)
owner_id = getenv("OWNER_ID", 739663149)
# remove_string = list(x for x in getenv("REMOVE_STRING", "").split(";"))
sudo_users = [owner_id]
temp_sudo = getenv("SUDO_USERS", None)
# tg_log = getenv("LOG_CHANNEL", None)
if temp_sudo is not None and len(temp_sudo) > 0:
    for each in temp_sudo.split(","):
        sudo_users.append(int(each))

# if ((token is None) ^ (session_string is None)) and api_id is None and api_hash is None and owner_id is None:
#     log.info("one or more variables is missing...")
#     exit(1)

# Initializing database...
try:
    # db = psycopg2.connect(database_url)
    db = sqlite3.connect("my.db")
    cursor = db.cursor()
    cursor.execute("create table if not exists copy(id integer primary key, mode varchar(10), from_chat bigint, from_chat_name varchar(255), to_chat bigint,to_chat_name varchar(255), start int, current int, stop int)")
    cursor.execute("create table if not exists sync(id integer primary key, from_chat bigint, from_chat_name varchar(255), to_chat bigint, to_chat_name varchar(255), last_id int)")
    db.commit()

except Exception as e:
    log.error(e)
    exit(1)


# Loading sync data
sync_data = {}
cursor.execute(f"select from_chat, to_chat from sync")
data_values = cursor.fetchall()
for each in data_values:
    try:
        sync_data[each[0]].append(each[1])
    except KeyError:
        sync_data[each[0]] = [each[1]]
from_chats = list(sync_data.keys())


class Bot(Client):

    def __init__(self, app_id = None, app_hash = None, string = None, token = None):
        super().__init__(
            name="nav",
            # api_id=app_id,
            # api_hash=app_hash,
            session_string = string,
            # bot_token = token,
            in_memory = True,
            plugins = dict(root="bot.plugins")
        )
    
    async def stop(self, *args):
        cursor.close()
        super().stop()

app = Bot(string=session_string)

