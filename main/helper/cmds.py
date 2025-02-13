import sys
import traceback
from functools import wraps

from pyrogram import filters

from config import ADMIN_IDS, BOT_ID, LOG_GRUP
from main import bot, fsub

from ..database import DB
from .tools import subcribe

BLACKLIST_CMD = [
    "start",
    "clone",
    "users",
    "broadcast",
    "eval",
    "ceval",
    "trash",
    "reboot",
    "update",
    "setdb",
    "getdb",
    "sh",
    "addprem",
    "delprem",
    "addexpired",
    "listprem",
    "addadmin",
    "deladmin",
    "getadmin",
    "listadmin",
    "help",
    "delbot",
    "info",
    "batch",
    "addseller",
    "getseller",
    "delseller",
    "genlink",
    "protect",
    "id",
    "addbutton",
    "delbutton",
    "getbutton",
    "listbutton",
    "addkonten",
    "delkonten",
    "getkonten",
    "limitkonten",
    "ping",
    "uptime",
    "limitbutton",
    "gban",
    "ungban",
    "gbanlist",
    "addpic",
    "delpic",
    "setmsg",
]


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    else:
        result.append(small_msg)

    return result


def capture_message(func):
    @wraps(func)
    async def capture(client, message):
        try:
            return await func(client, message)
        except Exception as err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error_feedback = split_limits(
                "❌**ERROR** | `{}` | `{}`\n\n<pre>{}</pre>\n\n<pre>{}</pre>\n".format(
                    (0 if not client.me else client.get_mention(client.me, logs=True)),
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await bot.send_message(LOG_GRUP, x)
            raise err

    return capture


def capture_callback(func):
    @wraps(func)
    async def capture(client, cq):
        try:
            return await func(client, cq)
        except Exception as err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error_feedback = split_limits(
                "❌**ERROR BANGSAT @Akwcuy** | `{}`\n\n<pre>{}</pre>".format(
                    (
                        0
                        if not cq.from_user
                        else bot.get_mention(cq.from_user, logs=True)
                    ),
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await bot.send_message(LOG_GRUP, x)
            raise err

    return capture


async def if_admins(_, client, message):
    admins = []
    owner_bot = DB.get_var(client.me.id, "OWNER")
    admin_bot = DB.get_list_from_var(client.me.id, "ADMINS")
    for x in admin_bot:
        if x not in admins:
            admins.append(x)
        if owner_bot not in admins:
            admins.append(owner_bot)
    is_user = message.from_user if message.from_user else message.sender_chat

    return is_user.id in admins


class FILTERS:
    PRIVATE = filters.private
    PRIVATE_FSUB = filters.private & subcribe
    ADMINS = filters.user(ADMIN_IDS)
    GROUP = filters.group
    OWNERS = filters.create(if_admins)
    POST_PRIVATE = filters.private & ~filters.command(BLACKLIST_CMD)
    POST_CHANNEL = filters.incoming & ~filters.command(BLACKLIST_CMD) & ~filters.private


class HANDLER:
    @staticmethod
    def BOTS(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            @capture_message
            async def wrapped_func(client, message):
                blocked = DB.get_list_from_var(BOT_ID, "BLOCKED")
                if message.from_user.id in blocked:
                    return
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def FSUB(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @fsub.on_message(message_filters)
            @capture_message
            async def wrapped_func(client, message):
                blocked = DB.get_list_from_var(BOT_ID, "BLOCKED")
                if message.from_user.id in blocked:
                    return
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def POST_CHANNEL():
        def wrapper(func):
            @fsub.on_message(FILTERS.POST_CHANNEL)
            @capture_message
            async def wrapped_func(client, message):
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def POST_PRIVATE():
        def wrapper(func):
            @fsub.on_message(FILTERS.POST_PRIVATE)
            @capture_message
            async def wrapped_func(client, message):
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def CALLBACK_BOT(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            @capture_callback
            async def wrapped_func(client, cq):
                return await func(client, cq)

            return wrapped_func

        return wrapper

    @staticmethod
    def CALLBACK_FSUB(command):
        def wrapper(func):
            @fsub.on_callback_query(filters.regex(command))
            @capture_callback
            async def wrapped_func(client, cq):
                return await func(client, cq)

            return wrapped_func

        return wrapper

    @staticmethod
    def REGEX_BOT(pattern, filter=False):
        def wrapper(func):
            message_filters = (
                filters.regex(pattern) & filter if filter else filters.regex(pattern)
            )

            @bot.on_message(message_filters)
            @capture_message
            async def wrapped_func(client, message):
                blocked = DB.get_list_from_var(BOT_ID, "BLOCKED")
                if message.from_user.id in blocked:
                    return
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def REGEX_FSUB(pattern, filter=False):
        def wrapper(func):
            message_filters = (
                filters.regex(pattern) & filter if filter else filters.regex(pattern)
            )

            @fsub.on_message(message_filters)
            @capture_message
            async def wrapped_func(client, message):
                blocked = DB.get_list_from_var(BOT_ID, "BLOCKED")
                if message.from_user.id in blocked:
                    return
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def MENTEN(func):
        async def function(client, message):
            kon = DB.get_var(client.me.id, "menten")
            if kon and message.from_user.id not in ADMIN_IDS:
                return await message.reply(
                    "<b>Bot sedang dalam proses Update.\n\nSilahkan tunggu info dari Owner.</b>"
                )
            return await func(client, message)

        return function

    @staticmethod
    def ADMINS(func):
        async def function(client, message):
            if not message.from_user:
                return
            kon = message.from_user.id
            if kon not in ADMIN_IDS:
                return
            return await func(client, message)

        return function

    @staticmethod
    def EXPIRED(func):
        async def function(client, message):
            expired_date = DB.get_expired_date(client.me.id)
            if expired_date is None:
                message.from_user.id
                owner = DB.get_var(client.me.id, "OWNER")
                adm = DB.get_list_from_var(client.me.id, "ADMINS")
                if message.from_user.id not in adm and message.from_user.id != owner:
                    return
                else:
                    return await message.reply(
                        "<blockquote><b>Maaf, masa aktif Bot Fsub Anda sudah habis!!\nSilahkan kontak @Akwcuy untuk memperpanjang masa aktif bot.</b></blockquote>"
                    )
            return await func(client, message)

        return function

    @staticmethod
    def SELLER(func):
        async def function(client, message):
            kon = message.from_user.id
            seles = DB.get_list_from_var(BOT_ID, "seller")
            if kon not in seles:
                return
            return await func(client, message)

        return function

    @staticmethod
    def BLOCKED(func):
        async def function(c, m):
            kon = m.from_user.id
            blus = DB.get_list_from_var(c.me.id, "BLOCKED")
            if kon in blus:
                return
            return await func(c, m)

        return function

    @staticmethod
    def BOT_BROADCAST(func):
        async def function(client, message):
            broadcast = DB.get_list_from_var(client.me.id, "BROADCAST_BOT")
            user = message.from_user
            if user.id not in broadcast:
                DB.add_to_var(client.me.id, "BROADCAST_BOT", user.id)
            return await func(client, message)

        return function

    @staticmethod
    def FSUB_BROADCAST(func):
        async def function(client, message):
            broadcast = DB.get_list_from_var(client.me.id, "BROADCAST")
            user = message.from_user
            if user.id not in broadcast:
                DB.add_to_var(client.me.id, "BROADCAST", user.id)
            return await func(client, message)

        return function
