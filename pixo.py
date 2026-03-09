import telebot
import yt_dlp
import os
from flask import Flask, request
import threading

# =========================
# Bot token
# =========================
TOKEN = "8624963114:AAH6Hg2rV6WIpPYzCvy4zpvBizWR03uKaWg"  
bot = telebot.TeleBot(TOKEN)

# =========================
# Download papkasi
# =========================
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Foydalanuvchilar
users = set()

# yt-dlp sozlamalari
ydl_opts = {
    "format": "best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
}

# =========================
# Video yuklash
# =========================
def download_video(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return filename, title

def safe_remove(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except:
        pass

# =========================
# /start handler
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"Salom, men Pixo video yuklovchi botman!\n"
        f"Foydalanuvchilar soni: {len(users)}"
    )

# =========================
# Video link handler
# =========================
@bot.message_handler(func=lambda m: True)
def handler(message):
    url = message.text.strip()
    users.add(message.from_user.id)

    msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")
    file_path = None
    try:
        file_path, title = download_video(url)
        with open(file_path, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                caption=title,
                supports_streaming=True
            )
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato:\n{e}", message.chat.id, msg.message_id)
    finally:
        safe_remove(file_path)

# =========================
# Telegram botni thread-da ishga tushirish
# =========================
def run_bot():
    bot.infinity_polling(skip_pending=True)

bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

# =========================
# Flask web server
# =========================
app = Flask(__name__)

@app.route("/")
def index():
    return "🚀 Pixo Video Bot ishlayapti!"

# =========================
# Flask server ishga tushishi
# =========================
if __name__ == "__main__":
    # Port Render avtomatik belgilaydi
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
