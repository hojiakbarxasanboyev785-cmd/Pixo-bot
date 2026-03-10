import telebot
import yt_dlp
import os
from flask import Flask
import threading

# =========================
# Bot token
# =========================
TOKEN = "8624963114:AAEvM6LxOwGYE346bOu7gvBgj8f6lZOmjBU"
bot = telebot.TeleBot(TOKEN)

# =========================
# Download papkasi
# =========================
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Foydalanuvchilar
users = set()

# =========================
# yt-dlp sozlamalari
# =========================
ydl_opts = {
    "format": "best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
}

# =========================
# Video yuklash funksiyasi
# =========================
def download_video(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return filename, title

# =========================
# Faylni o'chirish
# =========================
def safe_remove(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except:
        pass

# =========================
# /start
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)

    text = (
        "✨ *Salom, men Pixo Video Botman!* ✨\n\n"
        "🎬 Instagram videolarini yuklab beraman.\n"
        f"👥 Foydalanuvchilar soni: *{len(users)}*\n\n"
        "⬇️ Instagram video linkini yuboring."
    )

    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# =========================
# Video yuklash
# =========================
@bot.message_handler(func=lambda message: True)
def download_handler(message):

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
                caption=f"🎬 Video: {title}\n📤 Yukladi: Pixo Bot",
                supports_streaming=True
            )

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(
            f"❌ Xato yuz berdi:\n{e}",
            message.chat.id,
            msg.message_id
        )

    finally:
        safe_remove(file_path)

# =========================
# Bot thread
# =========================
def run_bot():
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot).start()

# =========================
# Flask Web Service
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Pixo bot ishlayapti!"

# =========================
# Server start
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
