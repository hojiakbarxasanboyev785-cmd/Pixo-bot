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

# yt-dlp sozlamalari faqat Instagram uchun
ydl_opts = {
    "format": "best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
    "ignoreerrors": True,
    "geo_bypass": True,
    "restrictfilenames": True
}

# =========================
# Video yuklash funksiyasi
# =========================
def download_instagram_video(url):
    if "instagram.com" not in url:
        raise ValueError("❌ Iltimos, faqat Instagram video linkini yuboring!")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if info is None:
            raise ValueError("❌ Video topilmadi yoki private hisob!")
        filename = ydl.prepare_filename(info)
        title = info.get("title", "Instagram Video")
    return filename, title

# =========================
# Faylni tozalash
# =========================
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
    start_text = (
        "✨ *Salom, men Pixo Instagram Video Botman!* ✨\n\n"
        "🎬 Men faqat Instagram videolarini yuklab bera olaman.\n"
        "📊 Foydalanuvchilar soni: *{users_count}*\n\n"
        "⬇️ Instagram video linkini shu yerga yuboring!"
    ).format(users_count=len(users))

    bot.send_message(
        message.chat.id,
        start_text,
        parse_mode="Markdown"
    )

# =========================
# Video link handler
# =========================
@bot.message_handler(func=lambda m: True)
def handler(message):
    url = message.text.strip()
    users.add(message.from_user.id)

    msg = bot.reply_to(message, "⏳ Video yuklanmoqda... Iltimos kuting! 🎬")
    file_path = None
    try:
        file_path, title = download_instagram_video(url)
        with open(file_path, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                caption=f"🎬 Video nomi: {title}\n📤 Yukladi: Pixo Bot",
                supports_streaming=True
            )
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato yuz berdi:\n{e}", message.chat.id, msg.message_id)
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
# Flask Web Service
# =========================
app = Flask(__name__)

@app.route("/")
def index():
    return "🚀 Pixo Instagram Video Bot ishlayapti!"

# =========================
# Flask server ishga tushishi
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
