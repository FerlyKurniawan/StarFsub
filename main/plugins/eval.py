import asyncio
import io
import os
import subprocess
import sys
import traceback
from time import perf_counter

from main import bot
from main.helper import HANDLER


@HANDLER.BOTS("trash")
@HANDLER.ADMINS
async def _(client: bot, message):
    return await cb_trash(client, message)


async def cb_trash(client, message):
    if message.reply_to_message:
        try:
            if len(message.command) < 2:
                if len(str(message.reply_to_message)) > 4096:
                    with io.BytesIO(
                        str.encode(str(message.reply_to_message))
                    ) as out_file:
                        out_file.name = "trash.txt"
                        return await message.reply_document(document=out_file)
                else:
                    return await message.reply(f"<pre>{message.reply_to_message}</pre>")
            else:
                value = eval(f"message.reply_to_message.{message.command[1]}")
                if len(str(value)) > 4096:
                    with io.BytesIO(str.encode(str(value))) as out_file:
                        out_file.name = "trash.txt"
                        return await message.reply_document(document=out_file)
                else:
                    return await message.reply(f"<pre>{value}</pre>")
        except Exception as error:
            return await message.reply(str(error))
    else:
        return await message.reply("noob")


@HANDLER.BOTS("shell")
@HANDLER.BOTS("sh")
@HANDLER.ADMINS
async def _(client: bot, message):
    return await cb_shell(client, message)


async def cb_shell(client, message):
    if len(message.command) < 2:
        return await message.reply("Noob!!")
    cmd_text = message.text.split(maxsplit=1)[1]
    text = f"<code>{cmd_text}</code>\n\n"
    start_time = perf_counter()
    try:
        stdout, stderr = await client.bash(cmd_text)
    except asyncio.TimeoutError:
        text += "<b>Timeout expired!!</b>"
        return await message.reply(text)
    finally:
        duration = perf_counter() - start_time
    if len(stdout) > 4096:
        anuk = await message.reply("<b>Oversize, sending file...</b>")
        with open("output.txt", "w") as file:
            file.write(stdout)
        await client.send_document(
            message.chat.id,
            "output.txt",
            caption=f"<b>Command completed in `{duration:.2f}` seconds.</b>",
            reply_to_message_id=message.id,
        )
        os.remove("output.txt")
        return await anuk.delete()
    else:
        text += f"<pre><code>{stdout}</code></pre>"

    if stderr:
        text += f"<blockquote>{stderr}</blockquote>"
    text += f"\n<b>Completed in `{duration:.2f}` seconds.</b>"
    return await message.reply(text)


@HANDLER.BOTS("eval")
@HANDLER.FSUB("ceval")
@HANDLER.ADMINS
async def _(client: bot, message):
    return await cb_evalusi(client, message)


async def cb_evalusi(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Noob!!")
    TM = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]
    reply_to_ = message.reply_to_message or message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await client.aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = exc or stderr or stdout or "Success"
    final_output = f"<b>OUTPUT</b>:\n<pre>{evaluation.strip()}</pre>"

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd[: 4096 // 4 - 1],
                disable_notification=True,
                quote=True,
            )
    else:
        await reply_to_.reply_text(final_output)
    return await TM.delete()


async def send_large_output(message, output):
    with io.BytesIO(str.encode(str(output))) as out_file:
        out_file.name = "update.txt"
        await message.reply_document(document=out_file)


@HANDLER.BOTS("reboot")
@HANDLER.BOTS("update")
@HANDLER.ADMINS
async def _(client: bot, message):
    return await cb_gitpull2(client, message)


async def cb_gitpull(client, message):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if "Already up to date." in str(out):
        return await message.reply(f"<pre>{out}</pre>")
    elif int(len(str(out))) > 4096:
        await send_large_output(m, out)
    else:
        await message.reply(f"<pre>{out}</pre>")
    await client.shell_exec("pkill -f gunicorn")
    os.execl(sys.executable, sys.executable, "-m", "main")


async def cb_gitpull2(client, message):
    if message.command[0] == "update":
        out, err = await client.shell_exec("git pull")
        if "Already up to date." in str(out):
            return await message.reply(f"<pre>{out}</pre>")
        elif len(str(out)) > 4096:
            await send_large_output(m, out)
        else:
            msg = f"<pre>{out}</pre>"
        try:
            oot, arr = await client.shell_exec("pkill -f gunicorn")
            msg += "\n".join(oot)
        except Exception as e:
            return await message.reply(f"Failed to stop Gunicorn: {str(e)}")
        await message.reply(
            msg
            + "\n<b>✅ Gunicorn stopped successfully. Trying to Update Userbot!!</b>"
        )
        os.execl(sys.executable, sys.executable, "-m", "main")
    elif message.command[0] == "reboot":
        oot, arr = await client.shell_exec("pkill -f gunicorn")
        await message.reply(
            "<b>✅ Gunicorn stopped successfully. Trying to restart Userbot!!</b>"
        )
        os.execl(sys.executable, sys.executable, "-m", "main")
