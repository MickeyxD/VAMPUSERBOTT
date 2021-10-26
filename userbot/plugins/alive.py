from userbot import *
from VAMPBOT.utils import *
from userbot.cmdhelp import CmdHelp
from telethon import events, version
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User

#-------------------------------------------------------------------------------

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "vamp User"

ludosudo = Config.SUDO_USERS

if ludosudo:
    sudou = "True"
else:
    sudou = "False"

aura = bot.uid

mention = f"[{DEFAULTUSER}](tg://user?id={aura})"


PM_IMG = "https://telegra.ph/file/fd0978ae951f06e2798ec.mp4"
pm_caption ="**ᴡ2ʜʙᴏᴛ Is ᴘʀᴇsᴇɴᴛɪɴɢ ʙᴇsᴛᴇsᴛ ʙᴏᴛ**\n\n"

pm_caption += f"**┏━━━━━━━━━━━━━┓**\n"
pm_caption += f"**┣★ ᴍᴀsᴛᴇʀ : {mention}**\n"
pm_caption += f"**┣★ ᴛᴇʟᴇᴛʜᴏɴ : `{version.__version__}`**\n"
pm_caption += f"**┣★ ᴡ2ʜʙᴏᴛ : {vampversion}**\n"
pm_caption += f"**┣★ sᴜᴅᴏ       : `{sudou}`**\n"
pm_caption += f"**┣★ ᴄʜᴀɴɴᴇʟ   : [Join Here](https://t.me/VAMPBOT_OFFICIAL)**\n"
pm_caption += f"**┣★ ᴄʀᴇᴀᴛᴏʀ    : [vamp Here](https://t.me/David99q)**\n"
pm_caption += f"**┗━━━━━━━━━━━━━┛**\n"

pm_caption += "    [✨REPO✨](https://github.com/D15H4NT0P/VAMPBOT) 🔹 [📜License📜](https://github.com/D15H4NT0P/VAMPBOT/blob/master/LICENSE)"


@bot.on(admin_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    await alive.get_chat()
    await alive.delete()
    """ For .alive command, check if the bot is running.  """
    await borg.send_file(alive.chat_id, PM_IMG, caption=pm_caption)
    await alive.delete()


CmdHelp("alive").add_command(
  'alive', None, 'Check weather the bot is alive or not'
).add_command(
  'vamp', None, 'Check weather the bot is alive or not. In your custom Alive Pic and Alive Msg'
).add_info(
  'Zinda Hai Kya Bro?'
).add()
