import os 
import time
import platform, socket, re, uuid, json, psutil, logging

from pymongo import MongoClient
from ..config import MONGO_DB_URI as smex

from pyrogram.types import Message
from pyrogram import filters, Client
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from sys import version as pyver

from FlameMusic import app, SUDOERS, BOT_ID, FlameMusic_START_TIME
from FlameMusic.FlameMusicUtilities.database.sudo import (get_sudoers, get_sudoers, remove_sudo)
from FlameMusic.FlameMusicUtilities.database.playlist import get_playlist_count
from FlameMusic.FlameMusicUtilities.database.gbanned import get_gbans_count
from FlameMusic.FlameMusicUtilities.database.chats import get_served_chats
from ..FlameMusicUtilities.helpers.time import get_readable_time
from ..FlameMusicUtilities.helpers.filters import command


@app.on_message(command("stats") & filters.user(SUDOERS))
async def get_statistic(_, message):
    m = await message.reply_text("🔄 **Getting bot stats...**")
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    blocked = await get_gbans_count()
    sudoers = await get_sudoers()
    j = 0
    for count, user_id in enumerate(sudoers, 0):
        try:                     
            user = await app.get_users(user_id)
            j += 1
        except Exception:
            continue                     
    modules_count ="20"
    sc = platform.system()
    arch = platform.machine()
    ram = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    bot_uptime = int(time.time() - FlameMusic_START_TIME)
    uptime = f"{get_readable_time((bot_uptime))}"
    hdd = psutil.disk_usage('/')
    total = (hdd.total / (1024.0 ** 3))
    total = str(total)
    used = (hdd.used / (1024.0 ** 3))
    used = str(used)
    free = (hdd.free / (1024.0 ** 3))
    free = str(free)
    msg = f"""
📊 **Current bot statistic:**

• **System Stats:**

**Uptime:** `{uptime}`
**System Proc:** Online
**Platform:** {sc}
**Storage:** used {used[:4]} GiB out of {total[:4]} GiB, free {free[:4]} GiB
**Architecture:** {arch}
**Ram:** {ram}
**Bot Version:** `latest version`
**Python Version:** `{pyver.split()[0]}`
**Pyrogram Version:** `{pyrover}`
**PyTgCalls Version:** `{pytover.__version__}`

• **Bot Stats:**

**Imported Modules:** `{modules_count}`
**Gbanned Users:** `{blocked}`
**Sudo Users:** `{j}`
**Authorized Chats:** `{len(served_chats)}`
"""
    served_chats.pop(1000)
    await m.edit(msg, disable_web_page_preview=True)
