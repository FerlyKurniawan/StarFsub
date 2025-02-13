import asyncio
import base64
import re

from pyrogram import enums, filters
from pyrogram.errors import FloodWait, UserNotParticipant

from config import BOT_ID
from main.database import DB


async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    return (base64_bytes.decode("ascii")).strip("=")


async def decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    return string_bytes.decode("ascii")


async def is_subscribed(_, client, message):
    if client.me.id == BOT_ID:
        return True
    admin = DB.get_var(client.me.id, "OWNER")
    links = [v for v in DB.get_list_from_var(client.me.id, "FORCE_SUB")]
    user_id = message.from_user.id
    cek_adm = DB.get_list_from_var(client.me.id, "ADMINS")
    if user_id == int(admin):
        return True
    if user_id in cek_adm:
        return True
    try:
        for link in links:
            member = await client.get_chat_member(link, user_id)
    except UserNotParticipant:
        return False

    return member.status in [
        enums.ChatMemberStatus.OWNER,
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.MEMBER,
    ]


async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    db = DB.get_var(client.me.id, "CH_BASE")
    while total_messages != len(message_ids):
        temb_ids = message_ids[total_messages : total_messages + 200]
        try:
            msgs = await client.get_messages(int(db), temb_ids)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(int(db), temb_ids)
        except BaseException:
            pass
        total_messages += len(temb_ids)
        messages.extend(msgs)
    return messages


async def get_message_id(client, message):
    db = DB.get_var(client.me.id, "CH_BASE")
    if message.forward_from_chat and message.forward_from_chat.id == int(db):
        return message.forward_from_message_id
    elif message.forward_from_chat or message.forward_sender_name or not message.text:
        return 0
    else:
        pattern = "https://t.me/(?:c/)?(.*)/(\\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id = matches[1]
        msg_id = int(matches[2])
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(db):
                return msg_id


subcribe = filters.create(is_subscribed)
