# Copyright (c) 2021 HEIMAN PICTURES

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from pyrogram import Client, filters
import logging


from configs import Config as C


# LMAO, This Is Logging 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Import From Framework
# from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from pyrogram.types import *

from database.broadcast import broadcast
from database.verifier import handle_user_status
from database.database import Database

LOG_CHANNEL = C.LOG_CHANNEL
AUTH_USERS = C.AUTH_USERS
DB_URL = C.DB_URL
DB_NAME = C.DB_NAME

db = Database(DB_URL, DB_NAME)

# Don't Change Anything, Except If You Want To Add Value
bot = Client('Feedback bot',
             api_id=C.API_ID,
             api_hash=C.API_HASH,
             bot_token=C.BOT_TOKEN)

donate_link=C.DONATE_LINK

owner_id=C.OWNER_ID

LOG_TEXT = "ID: <code>{}</code>\nFirst Name: <a href='tg://user?id={}'>{}{}</a>\nDC ID: <code>{}</code>"

IF_TEXT = "<b>Message from:</b> {}\n<b>Name:</b> {}\n\n{}"

IF_CONTENT = "<b>Message from:</b> {} \n<b>Name:</b> {}"

# Callback
@bot.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    user_id = cb.from_user.id
    if "closeMeh" in cb.data:
        await cb.message.delete(True)
    elif "notifon" in cb.data:
        notif = await db.get_notif(cb.from_user.id)
        if notif is True:
            # 
            await db.set_notif(user_id, notif=False)
        else:
            # 
            await db.set_notif(user_id, notif=True)
        await cb.message.edit(
            f"`Here You Can Set Your Settings:`\n\nSuccessfully setted notifications to **{await db.get_notif(user_id)}**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"NOTIFICATION  {'🔔' if ((await db.get_notif(user_id)) is True) else '🔕'}",
                            callback_data="notifon",
                        )
                    ],
                    [InlineKeyboardButton("❎", callback_data="closeMeh")],
                ]
            ),
        )
        await cb.answer(
            f"Successfully setted notifications to {await db.get_notif(user_id)}"
        )
        
        
@bot.on_message(filters.private)
async def _(bot, cmd):
    await handle_user_status(bot, cmd)

@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    chat_id = message.from_user.id
    # Adding to DB
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
        )
        return
      
    # 
    ban_status = await db.get_ban_status(chat_id)
    is_banned = ban_status['is_banned']
    ban_duration = ban_status['ban_duration']
    ban_reason = ban_status['ban_reason']
    if is_banned is True:
        await message.reply_text(f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**")
        return
      
    await bot.send_message(
        chat_id=owner_id,
        text=LOG_TEXT.format(message.chat.id,message.chat.id,message.chat.first_name,message.chat.last_name,message.chat.dc_id),
        parse_mode="html"
    )
    await message.reply_text(
        text="**Hi {}!**\n".format(message.chat.first_name)+C.START,
        reply_markup=InlineKeyboardMarkup([
            [ InlineKeyboardButton(text="🛠SUPPORT🛠", url=f"{C.SUPPORT_GROUP}"), InlineKeyboardButton(text="📮UPDATES📮", url=f"{C.UPDATE_CHANNEL}")]
        ])
    )

@bot.on_message(filters.command('help') & filters.private)
async def help(bot, message):
    chat_id = message.from_user.id
    # Adding to DB
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
        )
    ban_status = await db.get_ban_status(chat_id)
    is_banned = ban_status['is_banned']
    ban_duration = ban_status['ban_duration']
    ban_reason = ban_status['ban_reason']
    if is_banned is True:
        await message.reply_text(f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**")
        return
      
    await message.reply_text(
        text=C.HELP,
        reply_markup=InlineKeyboardMarkup([
            [ InlineKeyboardButton(text="🛠SUPPORT🛠", url=f"{C.SUPPORT_GROUP}"), InlineKeyboardButton(text="📮UPDATES📮", url=f"{C.UPDATE_CHANNEL}")]
        ])
    )


@bot.on_message(filters.command('donate') & filters.private)
async def donate(bot, message):
    chat_id = message.from_user.id
    # Adding to DB
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
        )
        
    ban_status = await db.get_ban_status(chat_id)
    is_banned = ban_status['is_banned']
    ban_duration = ban_status['ban_duration']
    ban_reason = ban_status['ban_reason']
    if is_banned is True:
        await message.reply_text(f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**")
        return
        
    await message.reply_text(
        text=C.DONATE + "If You Liked This Bot You Can Also Donate Creator through BTC `3AKE4bNwb9TsgaofLQxHAGCR9w2ftwFs2R`",
        reply_markup=InlineKeyboardMarkup([
            [ InlineKeyboardButton(text="DONATE", url=f"{donate_link}")]
        ])
    )


@bot.on_message(filters.private & filters.text)
async def pm_text(bot, message):
    chat_id = message.from_user.id
    # Adding to DB
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
        )
    ban_status = await db.get_ban_status(chat_id)
    is_banned = ban_status['is_banned']
    ban_duration = ban_status['ban_duration']
    ban_reason = ban_status['ban_reason']
    if is_banned is True:
        await message.reply_text(f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**")
        return
      
    if message.from_user.id == owner_id:
        return
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    await bot.send_message(
        chat_id=owner_id,
        text=IF_TEXT.format(reference_id, info.first_name, message.text),
        parse_mode="html"
    )


@bot.on_message(filters.private & filters.media)
async def pm_media(bot, message):
    chat_id = message.from_user.id
    # Adding to DB
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
        )
    ban_status = await db.get_ban_status(chat_id)
    is_banned = ban_status['is_banned']
    ban_duration = ban_status['ban_duration']
    ban_reason = ban_status['ban_reason']
    if is_banned is True:
        await message.reply_text(f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**")
        return
      
    if message.from_user.id == owner_id:
        await replay_media(bot, message)
        return
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    await bot.copy_message(
        chat_id=owner_id,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        caption=IF_CONTENT.format(reference_id, info.first_name),
        parse_mode="html"
    )


@bot.on_message(filters.user(owner_id) & filters.text)
async def reply_text(bot, message):
    chat_id = message.from_user.id
    # Adding to DB
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
        )
    
    reference_id = True
    if message.reply_to_message is not None:
        file = message.reply_to_message
        try:
            reference_id = file.text.split()[2]
        except Exception:
            pass
        try:
            reference_id = file.caption.split()[2]
        except Exception:
            pass
        await bot.send_message(
            chat_id=int(reference_id),
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            text=message.text
        )


@bot.on_message(filters.user(owner_id) & filters.media)
async def replay_media(bot, message):
    chat_id = message.from_user.id
    # Adding to DB
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
        )
    reference_id = True
    if message.reply_to_message is not None:
        file = message.reply_to_message
        try:
            reference_id = file.text.split()[2]
        except Exception:
            pass
        try:
            reference_id = file.caption.split()[2]
        except Exception:
            pass
        await bot.copy_message(
            chat_id=int(reference_id),
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            parse_mode="html"
        )


@bot.on_message(filters.user(owner_id) & filters.command("settings") & filters.private)
async def opensettings(bot, cmd):
    user_id = cmd.from_user.id
    # Adding to DB
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
        )
    await cmd.reply_text(
        f"⚙ `Here You Can Set Your Settings:` ⚙\n\nSuccessfully setted notifications to **{await db.get_notif(user_id)}**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"NOTIFICATION  {'🔔' if ((await db.get_notif(user_id)) is True) else '🔕'}",
                        callback_data="notifon",
                    )
                ],
                [InlineKeyboardButton("❎", callback_data="closeMeh")],
            ]
        ),
    )


@bot.on_message(filters.private & filters.command("broadcast"))
async def broadcast_handler_open(_, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if m.reply_to_message is None:
        await m.delete()
        return
    await broadcast(m, db)


@bot.on_message(filters.private & filters.command("stats"))
async def sts(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    await m.reply_text(
        text=f"**Total Users in Database 📂:** `{await db.total_users_count()}`\n\n**Total Users with Notification Enabled 🔔 :** `{await db.total_notif_users_count()}`",
        parse_mode="Markdown",
        quote=True,
    )


@bot.on_message(filters.private & filters.command("ban_user"))
async def ban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban 🛑 any user from the bot 🤖.\n\nUsage:\n\n`/ban_user user_id ban_duration ban_reason`\n\nEg: `/ban_user 1234567 28 You misused me.`\n This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = " ".join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."

        try:
            await c.send_message(
                user_id,
                f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**",
            )
            ban_log_text += "\n\nUser notified successfully!"
        except BaseException:
            traceback.print_exc()
            ban_log_text += (
                f"\n\n ⚠️ User notification failed! ⚠️ \n\n`{traceback.format_exc()}`"
            )
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(ban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True,
        )


@bot.on_message(filters.private & filters.command("unban_user"))
async def unban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban 😃 any user.\n\nUsage:\n\n`/unban_user user_id`\n\nEg: `/unban_user 1234567`\n This will unban user with id `1234567`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user 🤪 {user_id}"

        try:
            await c.send_message(user_id, f"Your ban was lifted!")
            unban_log_text += "\n\n✅ User notified successfully! ✅"
        except BaseException:
            traceback.print_exc()
            unban_log_text += (
                f"\n\n⚠️ User notification failed! ⚠️\n\n`{traceback.format_exc()}`"
            )
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(unban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"⚠️ Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True,
        )


@bot.on_message(filters.private & filters.command("banned_users"))
async def _banned_usrs(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ""
    async for banned_user in all_banned_users:
        user_id = banned_user["id"]
        ban_duration = banned_user["ban_status"]["ban_duration"]
        banned_on = banned_user["ban_status"]["banned_on"]
        ban_reason = banned_user["ban_status"]["ban_reason"]
        banned_usr_count += 1
        text += f"> **User_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, **Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s) 🤭: `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open("banned-users.txt", "w") as f:
            f.write(reply_text)
        await m.reply_document("banned-users.txt", True)
        os.remove("banned-users.txt")
        return
    await m.reply_text(reply_text, True)

    return


bot.run()
