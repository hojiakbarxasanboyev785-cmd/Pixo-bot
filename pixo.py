import telebot
import yt_dlp
import os
from flask import Flask
import threading

# =========================
# Bot token
# =========================
TOKEN = "8624963114:AAF1wIyfnfoY7Qu-Ct6jl6hXJQzD6Au9vB0"
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
    "format": "bestvideo+bestaudio/best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(id)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
    "nocheckcertificate": True,
    "geo_bypass": True,
    "cookiefile": "cookies.txt"  # agar cookies.txt bo'lsa ishlatadi
}

# =========================
# Video yuklash funksiyasi
# =========================
def download_video(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        title = info.get("title", "Instagram Video")
    return filename, title

# =========================
# Faylni o‘chirish
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
        "✨ *Assalomu alaykum!* ✨\n\n"
        "🤖 *Men Pixo Botman*\n"
        "📥 Instagram videolarini yuklab beraman.\n\n"
        f"👥 Foydalanuvchilar: *{len(users)}*\n\n"
        "⬇️ Instagram Reel yoki Post link yuboring!"
    )

    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# =========================
# Link handler
# =========================
@bot.message_handler(func=lambda m: True)
def handler(message):

    url = message.text.strip()
    users.add(message.from_user.id)

    if "instagram.com" not in url:
        bot.reply_to(message, "❌ Faqat Instagram link yuboring.")
        return

    msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")

    file_path = None

    try:
        file_path, title = download_video(url)

        with open(file_path, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                caption=f"🎬 {title}\n🤖 Pixo Bot",
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
# Telegram bot thread
# =========================
def run_bot():
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot).start()

# =========================
# Flask web service
# =========================
app = Flask(__name__)

@app.route("/")
def index():
    return "🚀 Pixo Instagram Video Bot ishlayapti!"

# =========================
# Flask start
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
