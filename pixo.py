import telebot
import yt_dlp
import requests
import os
from flask import Flask
import threading

TOKEN = os.environ.get("8624963114:AAF1wIyfnfoY7Qu-Ct6jl6hXJQzD6Au9vB0")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
users = set()

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ==============================
# 1-usul: yt-dlp
# ==============================
def download_ytdlp(url, file_path):
    ydl_opts = {
        "format": "best",
        "outtmpl": file_path,
        "quiet": True,
        "nocheckcertificate": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# ==============================
# 2-usul: cobalt.tools (zapas)
# ==============================
def download_cobalt(url, file_path):
    response = requests.post(
        "https://api.cobalt.tools/",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json={"url": url},
        timeout=30
    )
    data = response.json()
    status = data.get("status")

    if status in ("stream", "redirect", "tunnel"):
        video_url = data["url"]
    elif status == "picker":
        video_url = data["picker"][0]["url"]
    else:
        raise Exception("Cobalt ham ishlamadi")

    r = requests.get(video_url, stream=True, timeout=60)
    with open(file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            f.write(chunk)

# ==============================
# Asosiy funksiya
# ==============================
def download_video(url, file_path):
    try:
        # Avval yt-dlp sinab ko'r
        download_ytdlp(url, file_path)
        if os.path.exists(file_path):
            return "yt-dlp"
    except Exception as e1:
        print(f"yt-dlp xato: {e1}")

    # Agar yt-dlp ishlamasa — cobalt
    download_cobalt(url, file_path)
    return "cobalt"

# ==============================
# /start
# ==============================
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(message.chat.id,
        "✨ *Assalomu alaykum!*\n\n"
        "🤖 *Men Pixo Botman*\n"
        "📥 Instagram videolarini yuklab beraman.\n\n"
        f"👥 Foydalanuvchilar: *{len(users)}*\n\n"
        "⬇️ Instagram Reel yoki Post link yuboring!",
        parse_mode="Markdown"
    )

# ==============================
# Link handler
# ==============================
@bot.message_handler(func=lambda m: True)
def handler(message):
    url = message.text.strip()
    users.add(message.from_user.id)

    if "instagram.com" not in url:
        bot.reply_to(message, "❌ Faqat Instagram link yuboring.")
        return

    msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")
    file_path = f"{DOWNLOAD_FOLDER}/{message.message_id}.mp4"

    try:
        usul = download_video(url, file_path)

        with open(file_path, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                caption=f"🎬 Instagram Video\n🤖 Pixo Bot",
                supports_streaming=True
            )

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(
            f"❌ Xato: {e}",
            message.chat.id,
            msg.message_id
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def run_bot():
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot).start()

@app.route("/")
def index():
    return "🚀 Pixo Bot ishlayapti!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
