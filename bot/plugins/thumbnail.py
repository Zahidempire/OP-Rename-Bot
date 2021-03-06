# (c) @Aadhi000

from bot.client import Client
from pyrogram import filters
from pyrogram import types
from bot.core.db.database import db
from bot.core.db.add import add_user_to_database


@Client.on_message(filters.command("show_thumbnail") & filters.private)
async def show_thumbnail(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sir :(")
    await add_user_to_database(c, m)
    thumbnail = await db.get_thumbnail(m.from_user.id)
    if not thumbnail:
        return await m.reply_text("ππΎπ π³πΈπ³π½'π ππ΄π π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ»!")
    await c.send_photo(m.chat.id, thumbnail, caption="π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ»!",
                       reply_markup=types.InlineKeyboardMarkup(
                           [[types.InlineKeyboardButton("π³π΄π»π΄ππ΄ ππ·ππΌπ±π½π°πΈπ»!",
                                                        callback_data="deleteThumbnail")]]
                       ))


@Client.on_message(filters.command("set_thumbnail") & filters.private)
async def set_thumbnail(c: Client, m: "types.Message"):
    if (not m.reply_to_message) or (not m.reply_to_message.photo):
        return await m.reply_text("ππ΄πΏπ»π ππΎ π°π½π πΈπΌπ°πΆπ΄ ππΎ ππ°ππ΄ πΈπ½ π°π π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ»!!")
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await db.set_thumbnail(m.from_user.id, m.reply_to_message.photo.file_id)
    await m.reply_text("Okay,\n"
                       "πΈ ππΈπ»π» πππ΄ ππ·πΈπ πΈπΌπ°πΆπ΄ π°π π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ».",
                       reply_markup=types.InlineKeyboardMarkup(
                           [[types.InlineKeyboardButton("π³π΄π»π΄ππ΄ ππ·ππΌπ±π½π°πΈπ»!",
                                                        callback_data="deleteThumbnail")]]
                       ))


@Client.on_message(filters.command("delete_thumbnail") & filters.private)
async def delete_thumbnail(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await db.set_thumbnail(m.from_user.id, None)
    await m.reply_text("πΎπΊπ°π,\n"
                       "πΈ π³π΄π»π΄ππ΄π³ π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ» π΅ππΎπΌ πΌπ π³π°ππ°π±π°ππ΄.")
