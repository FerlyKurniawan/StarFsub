import asyncio

from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from main import BOT_ID, logger
from main.database import DB
from main.helper import HANDLER


@HANDLER.FSUB("users")
@HANDLER.EXPIRED
async def get_users(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    adm = DB.get_list_from_var(client.me.id, "ADMINS")
    if message.from_user.id not in adm and message.from_user.id != owner:
        return
    msg = await client.send_message(message.chat.id, "Tunggu Sebentar...")
    users = DB.get_list_from_var(client.me.id, "BROADCAST")
    return await msg.edit(f"{len(users)} user")


@HANDLER.BOTS("buser")
@HANDLER.ADMINS
async def get_users(client, message):
    msg = await message.reply(message.chat.id, "Tunggu Sebentar...")
    users = DB.get_list_from_var(client.me.id, "BROADCAST_BOT")
    return await msg.edit(f"{len(users)} user")


@HANDLER.FSUB("broadcast")
@HANDLER.EXPIRED
async def _(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    adm = DB.get_list_from_var(client.me.id, "ADMINS")
    if message.from_user.id not in adm and message.from_user.id != owner:
        return
    if not message.reply_to_message:
        return await message.reply("`/broadcast [Reply ke pesan]`")
    query = DB.get_list_from_var(client.me.id, "BROADCAST")
    broadcast_msg = message.reply_to_message
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0
    pls_wait = await message.reply("Tunggu Sebentar...")
    for chat_id in query:
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await broadcast_msg.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            DB.remove_from_var(client.me.id, "BROADCAST", chat_id)
            blocked += 1
        except InputUserDeactivated:
            DB.remove_from_var(client.me.id, "BROADCAST", chat_id)
            deleted += 1
        except:
            unsuccessful += 1
        total += 1
    status = f"""**Berhasil Mengirim pesan ke:

Berhasil: {successful}
Gagal: {unsuccessful}
Pengguna Diblokir: {blocked}
Akun Dihapus: {deleted}
Total Pengguna: {total}**"""
    return await pls_wait.edit(status)


@HANDLER.BOTS("broadcast")
@HANDLER.ADMINS
async def _(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply Goblok")
    query = DB.get_list_from_var(client.me.id, "BROADCAST_BOT")
    broadcast_msg = message.reply_to_message
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0

    pls_wait = await message.reply("SABAR NGENTOT")
    for chat_id in query:
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await broadcast_msg.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            DB.remove_from_var(client.me.id, "BROADCAST_BOT", chat_id)
            blocked += 1
        except InputUserDeactivated:
            DB.remove_from_var(client.me.id, "BROADCAST_BOT", chat_id)
            deleted += 1
        except:
            unsuccessful += 1
        total += 1

    status = f"""**Berhasil Mengirim pesan ke:

Berhasil: {successful}
Gagal: {unsuccessful}
Pengguna Diblokir: {blocked}
Akun Dihapus: {deleted}
Total Pengguna: {total}**"""

    return await pls_wait.edit(status)


@HANDLER.FSUB("addadmin")
@HANDLER.EXPIRED
async def add_admin_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return
    if len(message.command) < 2:
        return await message.reply("Balas pesan pengguna atau berikan user_id.")
    ids = int(message.command[1])
    adm = DB.get_list_from_var(client.me.id, "ADMINS")
    if ids not in adm:
        DB.add_to_var(client.me.id, "ADMINS", ids)
        return await message.reply(f"User {ids} Berhasil ditambahkan menjadi admin.")
    else:
        return await message.reply(f"User {ids} Sudah ada di daftar Admin.")


@HANDLER.FSUB("deladmin")
@HANDLER.EXPIRED
async def del_admin_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return
    if len(message.command) < 2:
        return await message.reply("Balas pesan pengguna atau berikan user_id.")
    ids = int(message.command[1])
    adm = DB.get_list_from_var(client.me.id, "ADMINS")
    if ids in adm:
        DB.remove_from_var(client.me.id, "ADMINS", ids)
        return await message.reply(f"User {ids} Berhasil Dihapus dari daftar Admin.")
    else:
        return await message.reply(f"User {ids} Tidak terdaftar di daftar Admin.")


@HANDLER.FSUB("getadmin")
@HANDLER.FSUB("listadmin")
@HANDLER.EXPIRED
async def cek_admin_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return
    msg = "**Daftar Admin**\n\n"
    adm = DB.get_list_from_var(client.me.id, "ADMINS")
    if not adm:
        return await message.reply("Belum ada Admin yang terdaftar.")
    for num, ex in enumerate(adm, start=1):
        try:
            afa = f"{num}.`{ex}`\n"
        except Exception:
            continue
        msg += afa
    return await message.reply(msg)


@HANDLER.BOTS("addseller")
@HANDLER.ADMINS
async def add_seller_sub(client, message):
    if len(message.command) < 2:
        return await message.reply("Balas pesan pengguna atau berikan user_id.")
    ids = int(message.command[1])
    seles = DB.get_list_from_var(BOT_ID, "seller")
    if ids not in seles:
        DB.add_to_var(BOT_ID, "seller", ids)
        return await message.reply(f"User {ids} Berhasil di tambahkan ke seller")
    else:
        return await message.reply(f"User {ids} Sudah menjadi seller")


@HANDLER.BOTS("delseller")
@HANDLER.ADMINS
async def del_seller_sub(client, message):
    if len(message.command) < 2:
        return await message.reply("Balas pesan pengguna atau berikan user_id.")
    ids = int(message.command[1])
    seles = DB.get_list_from_var(BOT_ID, "seller")
    if ids in seles:
        DB.remove_from_var(BOT_ID, "seller", ids)
        return await message.reply(f"{ids} Berhasil di hapus dari seller")
    else:
        return await message.reply(f"{ids} Bukan bagian dari seller")


@HANDLER.BOTS("getseller")
@HANDLER.BOTS("listseller")
@HANDLER.ADMINS
async def del_seller_sub(client, message):
    msg = "**Daftar Seller**\n\n"
    seles = DB.get_list_from_var(BOT_ID, "seller")
    if not seles:
        return await message.reply("Belum ada Seller yang terdaftar.")
    for num, ex in enumerate(seles, start=1):
        try:
            afa = f"{num}.`{ex}`\n"
        except Exception:
            continue
        msg += afa
    return await message.reply(msg)


@HANDLER.FSUB("protect")
@HANDLER.EXPIRED
async def set_protect(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    adm = DB.get_list_from_var(client.me.id, "ADMINS")
    if message.from_user.id not in adm and message.from_user.id != owner:
        return
    if len(message.command) < 2:
        return await message.reply("`/protect [True/False]`")
    jk = message.command[1]
    if jk in ["True", "False"]:
        DB.set_var(client.me.id, "PROTECT", jk)
        return await message.reply(f"Berhasil mengatur protect menjadi {jk}")
    else:
        return await message.reply(
            f"{jk} Format salah, Gunakan `/protect [True/False]`."
        )


@HANDLER.FSUB("addbutton")
@HANDLER.EXPIRED
async def add_sub_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return
    if len(message.command) < 2:
        return await message.reply("Gunakan Format `/addbutton -100xxxx`")
    ids = int(message.command[1])
    x = DB.get_list_from_var(client.me.id, "FORCE_SUB")
    s = DB.get_var(client.me.id, "MAX_SUB")
    if len(x) == s:
        return await message.reply(
            f"Batas fsub {s} telah tercapai, Silahkan Hubungi Owner Bot Fsub untuk bantuan."
        )
    if ids not in x:
        try:
            await client.export_chat_invite_link(ids)
            DB.add_to_var(client.me.id, "FORCE_SUB", ids)
            return await message.reply(f"{ids} Berhasil ditambahkan di Fsub")
        except:
            return await message.reply(f"Maaf saya bukan admin di `{ids}`")
    else:
        return await message.reply(
            f"`{ids}` Sudah ada dilist Fsub\nSilahkan ketik `/listbutton` untuk melihat daftar Fsub."
        )


@HANDLER.FSUB("delbutton")
@HANDLER.EXPIRED
async def del_sub_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return
    if len(message.command) < 2:
        return await message.reply("Gunakan format `/delbutton -100xxxx`")
    ids = int(message.command[1])
    x = DB.get_list_from_var(client.me.id, "FORCE_SUB")
    if ids in x:
        DB.remove_from_var(client.me.id, "FORCE_SUB", ids)
        return await message.reply(f"{ids} Telah di dihapus dari Fsub")
    else:
        return await message.reply(f"{ids} Tidak ditemukan di daftar Fsub")


@HANDLER.FSUB("getbutton")
@HANDLER.FSUB("listbutton")
@HANDLER.EXPIRED
async def cek_sub_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return

    adm = DB.get_list_from_var(client.me.id, "FORCE_SUB")
    if not adm:
        return await message.reply("List Kosong")

    buttons = []
    temp_row = []

    for num, chat_id in enumerate(adm, start=1):
        try:
            chat = await client.get_chat(chat_id)
            invite_link = await client.export_chat_invite_link(chat_id)
            temp_row.append(
                InlineKeyboardButton(text=f"{num}. {chat.title}", url=invite_link)
            )

            if len(temp_row) == 2 or num == len(adm):
                buttons.append(temp_row)
                temp_row = []

        except Exception as e:
            logger.error(f"Error for chat {chat_id}: {e}")
            continue

    reply_markup = InlineKeyboardMarkup(buttons)

    return await message.reply(
        "**List Grup Force Subscribe**\n", reply_markup=reply_markup
    )


@HANDLER.BOTS("gban")
@HANDLER.ADMINS
async def giben(client, message):
    if len(message.command) < 2:
        return await message.reply("Berikan id pengguna.\nContoh: /gban 20731464")
    user_id = message.command[1]
    blocked = DB.get_list_from_var(BOT_ID, "BLOCKED")
    try:
        org = await client.get_users(user_id)
        if org.id in blocked:
            return await message.reply_text("Pengguna sudah didalam blacklist.")
        DB.add_to_var(BOT_ID, "BLOCKED", org.id)
        return await message.reply_text("Added to blacklist-users.")
    except Exception:
        org = user_id
        if org in blocked:
            return await message.reply_text("Pengguna sudah didalam blacklist.")
        DB.add_to_var(BOT_ID, "BLOCKED", org)
        return await message.reply_text("Added to blacklist-users.")


@HANDLER.BOTS("gbanlist")
@HANDLER.ADMINS
async def listgiben(client, message):
    blocked = DB.get_list_from_var(BOT_ID, "BLOCKED")
    if not blocked:
        return await message.reply_text("Belum ada pengguna yang diblacklist!!")
    text = ""
    for count, chat_id in enumerate(blocked, start=1):
        text += "<b>• {}. [<code>{}</code>]</b>\n".format(count, chat_id)
    return await message.reply_text(text)


@HANDLER.BOTS("ungban")
@HANDLER.ADMINS
async def ungban(client, message):
    if len(message.command) < 2:
        return await message.reply("Berikan id pengguna.\nContoh: /ungban 20731464")
    user_id = message.command[1]
    blocked = DB.get_list_from_var(BOT_ID, "BLOCKED")
    try:
        org = await client.get_users(user_id)
        if org.id not in blocked:
            return await message.reply_text("Pengguna tidak didalam blacklist.")
        DB.remove_from_var(BOT_ID, "BLOCKED", org.id)
        return await message.reply_text("Removed from blacklist-users.")
    except Exception:
        org = user_id
        if org not in blocked:
            return await message.reply_text("Pengguna tidak didalam blacklist.")
        DB.remove_from_var(BOT_ID, "BLOCKED", org)
        return await message.reply_text("Removed from blacklist-users.")


@HANDLER.FSUB("addkonten")
@HANDLER.EXPIRED
async def add_sub_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return
    if len(message.command) < 2:
        return await message.reply("Gunakan Format `/addkonten -100xxxx`")
    ids = int(message.command[1])
    x = DB.get_list_from_var(client.me.id, "KONTEN")
    s = DB.get_var(client.me.id, "MAX_KONTEN")
    if len(x) == s:
        return await message.reply(
            f"Batas konten {s} telah tercapai, Silahkan Hubungi Owner Bot Fsub untuk bantuan."
        )
    if ids not in x:
        try:
            await client.export_chat_invite_link(ids)
            DB.add_to_var(client.me.id, "KONTEN", ids)
            return await message.reply(f"{ids} Berhasil ditambahkan ke Channel Konten.")
        except:
            return await message.reply(f"Maaf saya bukan admin di `{ids}`")
    else:
        return await message.reply(
            f"`{ids}` Sudah ada dilist Channel Konten\nSilahkan ketik `/listkonten` untuk melihat daftar Channel Konten."
        )


@HANDLER.FSUB("delkonten")
@HANDLER.EXPIRED
async def del_sub_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return
    if len(message.command) < 2:
        return await message.reply("Gunakan format `/delkonten -100xxxx`")
    ids = int(message.command[1])
    x = DB.get_list_from_var(client.me.id, "KONTEN")
    if ids in x:
        DB.remove_from_var(client.me.id, "KONTEN", ids)
        return await message.reply(f"{ids} Telah di dihapus dari Channel Konten")
    else:
        return await message.reply(f"{ids} Tidak ditemukan di daftar Channel Konten")


@HANDLER.FSUB("getkonten")
@HANDLER.EXPIRED
async def cek_sub_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return
    msg = "**List Fsub / konten**\n\n"
    adm = DB.get_list_from_var(client.me.id, "KONTEN")
    if not adm:
        return await message.reply("List Kosong")
    for num, ex in enumerate(adm, start=1):
        try:
            jj = await client.get_chat(ex)
            afa = f"{num}. `{jj.id}` | {jj.title}\n"
        except Exception:
            afa = f"{num}. `{jj.id}`\n"
        msg += afa
    return await message.reply(msg)


@HANDLER.FSUB("limitkonten")
@HANDLER.EXPIRED
async def cek_sub_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return
    adm = DB.get_var(client.me.id, "MAX_KONTEN")
    return await message.reply(f"Batas Channel konten Anda {adm}")


@HANDLER.FSUB("limitbutton")
@HANDLER.EXPIRED
async def cek_sub_bot(client, message):
    owner = DB.get_var(client.me.id, "OWNER")
    if message.from_user.id != owner:
        return
    adm = DB.get_var(client.me.id, "MAX_SUB")
    return await message.reply(f"Batas button Anda {adm}")
