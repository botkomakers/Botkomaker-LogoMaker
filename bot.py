
from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from config import API_ID, API_HASH, BOT_TOKEN

FLAME_STYLES = {
    "fluffy": "fluffy-logo",
    "runner": "runner-logo",
    "glow": "glow-logo",
    "ice": "ice-logo",
    "metal": "steel-logo",
    "3d": "3d-logo"
}

bot = Client("advanced_logo_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply_text("স্বাগতম! `/logo <text>` দিয়ে লোগো বানাও।\nস্টাইল দিতে চাইলে `/style 3d`, `/style fluffy` এসব দাও।")

@bot.on_message(filters.command("style"))
async def set_style(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("স্টাইল দিন যেমন `/style 3d`")
    style = m.command[1].lower()
    if style not in FLAME_STYLES:
        return await m.reply_text("ভুল স্টাইল! Valid: " + ", ".join(FLAME_STYLES))
    bot.db[m.from_user.id] = style
    await m.reply_text(f"স্টাইল `{style}` সেট হয়েছে!")

@bot.on_message(filters.command("logo"))
async def logo(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("লেখা দিন! যেমন `/logo আমার নাম`")

    text = " ".join(m.command[1:])
    style = bot.db.get(m.from_user.id, "fluffy")  # default style
    logo_url = f"https://flamingtext.com/net-fu/proxy_form.cgi?script={FLAME_STYLES[style]}&text={text}&_loc=generate&imageoutput=true"

    await m.reply_photo(photo=logo_url, caption=f"`{text}` এর `{style}` লোগো!")

# ইন-মেমরি ডেটাবেস
bot.db = {}

bot.run()





# Dummy HTTP server for Render port binding
import os
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run).start()