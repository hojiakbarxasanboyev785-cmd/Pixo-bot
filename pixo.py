import telebot
import yt_dlp
import os

# =========================
# BOT TOKEN
# =========================
BOT_TOKEN = "8624963114:AAF1wIyfnfoY7Qu-Ct6jl6hXJQzD6Au9vB0"
bot = telebot.TeleBot(BOT_TOKEN)

# =========================
# DOWNLOAD PAPKA
# =========================
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# =========================
# YT-DLP SOZLAMALARI
# =========================
ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(id)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
    "cookiefile": "cookies.txt",   # agar cookies.txt bo‘lsa ishlatadi
    "nocheckcertificate": True,
    "geo_bypass": True
}

# =========================
# START
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    text = (
        "✨ *Assalomu alaykum!* ✨\n\n"
        "🤖 *Men Pixo Botman*\n"
        "📥 Instagram videolarini tez va oson yuklab beraman.\n\n"
        "📌 *Qanday ishlaydi?*\n"
        "1️⃣ Instagram Reel yoki Post linkini yuboring\n"
        "2️⃣ Men videoni yuklab olaman\n"
        "3️⃣ Sizga tayyor video yuboraman 🎬\n\n"
        "🚀 Instagram link yuboring!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# =========================
# VIDEO YUKLASH FUNKSIYA
# =========================
def download_video(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        title = info.get("title", "Instagram Video")
    return filename, title

# =========================
# LINK QABUL QILISH
# =========================
@bot.message_handler(func=lambda m: True)
def handle_link(message):

    url = message.text.strip()

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
            f"❌ Xatolik yuz berdi:\n{e}",
            message.chat.id,
            msg.message_id
        )

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

# =========================
# BOT START
# =========================
print("Pixo bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)
