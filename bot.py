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
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await bot.send_message(
        chat_id=owner_id,
        text=LOG_TEXT.format(message.chat.id,message.chat.id,message.chat.first_name,message.chat.last_name,message.chat.dc_id),
        parse_mode="html"
    )
    await message.reply_text(
        text="**Hi {}!**\n".format(message.chat.first_name)+C.START,
        reply_markup=InlineKeyboardMarkup([
            [ InlineKeyboardButton(text="🛠SUPPORT🛠", url=f"https://t.me/HeimanSupport/"), InlineKeyboardButton(text="📮UPDATES📮", url=f"https://t.me/HeimanSupports/")]
        ])
    )


@bot.on_message(filters.command('help') & filters.private)
async def help(bot, message):
    await message.reply_text(
        text=C.HELP,
        reply_markup=InlineKeyboardMarkup([
            [ InlineKeyboardButton(text="🛠SUPPORT🛠", url=f"https://t.me/HeimanSupport/"), InlineKeyboardButton(text="📮UPDATES📮", url=f"https://t.me/HeimanSupports/")]
        ])
    )


@bot.on_message(filters.command('donate') & filters.private)
async def donate(bot, message):
    await message.reply_text(
        text=C.DONATE,
        reply_markup=InlineKeyboardMarkup([
            [ InlineKeyboardButton(text="DONATE", url=f"{donate_link}")],
            [ InlineKeyboardButton(text="DONATE", url=f"https://t.me/HeimanSupport/")]
        ])
    )


@bot.on_message(filters.private & filters.text)
async def pm_text(bot, message):
    if message.from_user.id == owner_id:
        await reply_text(bot, message)
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
            text=message.text,
            chat_id=int(reference_id)
        )


@bot.on_message(filters.user(owner_id) & filters.media)
async def replay_media(bot, message):
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

bot.run()
