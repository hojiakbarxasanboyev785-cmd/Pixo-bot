import telebot
import requests
from bs4 import BeautifulSoup
import os
from flask import Flask
import threading

# =========================
# BOT TOKEN
# =========================
TOKEN = "8624963114:AAEvM6LxOwGYE346bOu7gvBgj8f6lZOmjBU"
bot = telebot.TeleBot(TOKEN)

# =========================
# Papka
# =========================
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

users = set()

# =========================
# Instagram video olish
# =========================
def download_instagram_video(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    video_tag = soup.find("meta", property="og:video")

    if not video_tag:
        raise Exception("Instagram videoni topa olmadim")

    video_url = video_tag["content"]

    video_data = requests.get(video_url).content

    file_path = f"{DOWNLOAD_FOLDER}/video.mp4"

    with open(file_path, "wb") as f:
        f.write(video_data)

    return file_path


# =========================
# START
# =========================
@bot.message_handler(commands=['start'])
def start(message):

    users.add(message.from_user.id)

    text = f"""
✨ Salom!

📥 Instagram video yuklovchi bot.

👥 Foydalanuvchilar: {len(users)}

📎 Instagram video linkini yuboring.
"""

    bot.send_message(message.chat.id, text)


# =========================
# LINK HANDLER
# =========================
@bot.message_handler(func=lambda m: True)
def handler(message):

    url = message.text.strip()

    if "instagram.com" not in url:
        bot.reply_to(message,"❌ Faqat Instagram link yuboring")
        return

    msg = bot.reply_to(message,"⏳ Video yuklanmoqda...")

    file_path = None

    try:

        file_path = download_instagram_video(url)

        with open(file_path,"rb") as video:
            bot.send_video(message.chat.id, video)

        bot.delete_message(message.chat.id,msg.message_id)

    except Exception as e:

        bot.edit_message_text(
            f"❌ Xato:\n{e}",
            message.chat.id,
            msg.message_id
        )

    if file_path and os.path.exists(file_path):
        os.remove(file_path)


# =========================
# BOT THREAD
# =========================
def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

# =========================
# WEB SERVER
# =========================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti"

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
