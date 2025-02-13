from pyrogram.enums import ChatType
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton

from main import logger
from main.database import DB


async def button_pas_pertama(client, message):
    temp = []
    links = []
    all_links = []
    new_keyboard = []
    get_subs = DB.get_list_from_var(client.me.id, "FORCE_SUB")

    for x in get_subs:
        try:
            info = await client.get_chat(int(x))
            link = getattr(
                info, "invite_link", None
            ) or await client.export_chat_invite_link(int(x))

            chat_type = info.type

            all_links.append((link, chat_type))
            try:
                await client.get_chat_member(int(x), message.from_user.id)
            except UserNotParticipant:
                links.append((link, chat_type))
        except Exception as er:
            logger.error(f"{str(er)}")

    owner = DB.get_var(client.me.id, "OWNER")
    adm = DB.get_list_from_var(client.me.id, "ADMINS")

    is_admin_or_owner = message.from_user.id in adm or message.from_user.id == int(
        owner
    )

    display_links = all_links if is_admin_or_owner else links

    keyboard = [
        InlineKeyboardButton(
            (
                f"{i + 1}. {'Group' if t == ChatType.SUPERGROUP else 'Channel'}"
                if is_admin_or_owner
                else f"Join {'Group' if t == ChatType.SUPERGROUP else 'Channel'}"
            ),
            url=h,
        )
        for i, (h, t) in enumerate(display_links)
    ]

    for i, board in enumerate(keyboard, start=1):
        temp.append(board)
        if i % 2 == 0:
            new_keyboard.append(temp)
            temp = []
        if i == len(keyboard):
            new_keyboard.append(temp)

    if is_admin_or_owner:
        new_keyboard.append(
            [
                InlineKeyboardButton("Info", callback_data="users_info"),
                InlineKeyboardButton("Settings", callback_data="users_settings"),
            ]
        )

    new_keyboard.append(
        [
            InlineKeyboardButton(
                text="Tutup",
                callback_data="closed",
            )
        ]
    )

    return new_keyboard


"""
async def force_button(client, message):
    temp = []
    new_keyboard = []
    links = []
    get_subs = DB.get_list_from_var(client.me.id, "FORCE_SUB")
    for x in get_subs:
        member = await client.get_chat_member(int(x), user_id)
        info = await client.get_chat(int(x))
        try:
            link = info.invite_link
        except:
            link = await client.export_chat_invite_link(int(x))
        links.append(link)
    keyboard = [InlineKeyboardButton("Join Sini Dulu", url=h) for h in links]
    for i, board in enumerate(keyboard, start=1):
        temp.append(board)
        if i % 2 == 0:
            new_keyboard.append(temp)
            temp = []
        if i == len(keyboard):
            new_keyboard.append(temp)
    owner = DB.get_var(client.me.id, "OWNER")
    adm = DB.get_list_from_var(client.me.id, "ADMINS")
    if message.from_user.id not in adm and message.from_user.id != int(owner):
        try:
            new_keyboard.append(
                [
                    InlineKeyboardButton(
                        "🔄 Coba Lagi",
                        url=f"https://t.me/{client.me.username}?start={message.command[1]}",
                    )
                ]
            )
        except IndexError:
            pass
    else:
        new_keyboard.append(
            [
                InlineKeyboardButton(
                    "Info",
                    callback_data="users_info",
                ),
                InlineKeyboardButton(
                    "F-Subs",
                    callback_data="users_settings",
                ),
            ]
        )
        new_keyboard.append(
            [
                InlineKeyboardButton(
                    text="❌ Tutup",
                    callback_data="closed",
                )
            ]
        )
    return new_keyboard
"""


async def force_button(client, message):
    new_keyboard = []
    temp = []
    links = []
    message.from_user.id
    get_subs = DB.get_list_from_var(client.me.id, "FORCE_SUB")

    for x in get_subs:
        try:
            try:
                await client.get_chat_member(int(x), message.from_user.id)
            except UserNotParticipant:
                info = await client.get_chat(int(x))
                link = getattr(
                    info, "invite_link", None
                ) or await client.export_chat_invite_link(int(x))
                links.append((link, info.type))
        except Exception as er:
            logger.error(f"{str(er)}")

    keyboard = [
        InlineKeyboardButton(
            f"Join {('Group' if t == ChatType.SUPERGROUP else 'Channel')}", url=h
        )
        for h, t in links
    ]

    for i, board in enumerate(keyboard, start=1):
        temp.append(board)
        if i % 2 == 0 or i == len(keyboard):
            new_keyboard.append(temp)
            temp = []

    owner = DB.get_var(client.me.id, "OWNER")
    adm = DB.get_list_from_var(client.me.id, "ADMINS")

    if message.from_user.id not in adm and message.from_user.id != int(owner):
        try:
            new_keyboard.append(
                [
                    InlineKeyboardButton(
                        "🔄 Coba Lagi",
                        url=f"https://t.me/{client.me.username}?start={message.command[1]}",
                    )
                ]
            )
        except IndexError:
            pass
    else:
        new_keyboard.extend(
            [
                [
                    InlineKeyboardButton("Info", callback_data="users_info"),
                    InlineKeyboardButton("Settings", callback_data="users_settings"),
                ],
                [InlineKeyboardButton(text="Close", callback_data="closed")],
            ]
        )

    return new_keyboard
