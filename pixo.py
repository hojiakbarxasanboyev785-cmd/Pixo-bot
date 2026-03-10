import telebot
import yt_dlp
import os
import threading
from flask import Flask

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

# Foydalanuvchilar (xotirda saqlanadi)
users = set()

# Telegram fayl hajmi limiti
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# =========================
# yt-dlp sozlamalari
# =========================
ydl_opts = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
    "merge_output_format": "mp4",
}

# =========================
# Video yuklash funksiyasi
# =========================
def download_video(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        title = info.get("title", "Video")

    # Extension farq qilishi mumkin — tekshiramiz
    if not os.path.exists(filename):
        base = os.path.splitext(filename)[0]
        for ext in [".mp4", ".webm", ".mkv", ".avi", ".mov"]:
            candidate = base + ext
            if os.path.exists(candidate):
                filename = candidate
                break

    return filename, title

# =========================
# Faylni xavfsiz o'chirish
# =========================
def safe_remove(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

# =========================
# /start
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    text = (
        "✨ *Salom! Men Pixo Video Botman!* ✨\n\n"
        "📥 Quyidagi platformalardan video yuklab beraman:\n"
        "• Instagram\n"
        "• YouTube\n"
        "• TikTok\n"
        "• Facebook\n\n"
        f"👥 Foydalanuvchilar soni: *{len(users)}*\n\n"
        "⬇️ Video havolasini yuboring!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# =========================
# /help
# =========================
@bot.message_handler(commands=["help"])
def help_cmd(message):
    text = (
        "ℹ️ *Yordam*\n\n"
        "1. Video havolasini menga yuboring\n"
        "2. Men videoni yuklab beraman\n\n"
        "⚠️ *Cheklovlar:*\n"
        "• Fayl 50MB dan oshmasligi kerak\n"
        "• Faqat ochiq (public) sahifalar ishlaydi\n\n"
        "🔗 Qo'llab-quvvatlanadigan saytlar:\n"
        "Instagram, YouTube, TikTok, Facebook va boshqalar"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# =========================
# Video yuklash handler
# =========================
@bot.message_handler(func=lambda message: True)
def download_handler(message):
    url = message.text.strip()
    users.add(message.from_user.id)

    # URL tekshiruvi
    allowed_domains = ["instagram.com", "youtube.com", "youtu.be", "tiktok.com", "facebook.com", "fb.watch"]
    if not any(domain in url for domain in allowed_domains):
        bot.reply_to(
            message,
            "❌ Noto'g'ri havola!\n\nFaqat Instagram, YouTube, TikTok yoki Facebook havolalarini yuboring."
        )
        return

    msg = bot.reply_to(message, "⏳ Video yuklanmoqda, iltimos kuting...")
    file_path = None

    try:
        file_path, title = download_video(url)

        # Fayl mavjudligini tekshir
        if not file_path or not os.path.exists(file_path):
            bot.edit_message_text(
                "❌ Video yuklab bo'lmadi. Havola ochiq ekanligini tekshiring.",
                message.chat.id,
                msg.message_id
            )
            return

        # Fayl hajmini tekshir
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            bot.edit_message_text(
                "❌ Fayl hajmi 50MB dan katta!\nTelegram bu o'lchamdagi fayllarni qabul qilmaydi.",
                message.chat.id,
                msg.message_id
            )
            return

        # Videoni yuborish
        bot.edit_message_text("📤 Video yuborilmoqda...", message.chat.id, msg.message_id)

        with open(file_path, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                caption=(
                    f"🎬 *{title}*\n\n"
                    f"📤 Yukladi: @PixoVideoBot"
                ),
                supports_streaming=True,
                parse_mode="Markdown"
            )

        bot.delete_message(message.chat.id, msg.message_id)

    except yt_dlp.utils.DownloadError as e:
        error_text = str(e)
        if "Private" in error_text or "login" in error_text.lower():
            user_msg = "❌ Bu video *xususiy* (private). Faqat ochiq videolarni yuklab olish mumkin."
        elif "not available" in error_text.lower():
            user_msg = "❌ Video mavjud emas yoki o'chirilgan."
        else:
            user_msg = f"❌ Yuklab bo'lmadi:\n`{error_text[:200]}`"

        bot.edit_message_text(user_msg, message.chat.id, msg.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.edit_message_text(
            f"❌ Xato yuz berdi:\n`{str(e)[:200]}`",
            message.chat.id,
            msg.message_id,
            parse_mode="Markdown"
        )

    finally:
        safe_remove(file_path)

# =========================
# Bot thread
# =========================
def run_bot():
    print("🤖 Bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot, daemon=True).start()

# =========================
# Flask Web Service (Render/Railway uchun)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return f"🚀 Pixo bot ishlayapti! Foydalanuvchilar: {len(users)}"

# =========================
# Server ishga tushirish
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Server port {port} da ishga tushdi")
    app.run(host="0.0.0.0", port=port)
