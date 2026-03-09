import telebot
import yt_dlp
import os
import re
import json
import threading
import logging
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# =========================
# Logging
# =========================
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# =========================
# Bot token
# =========================
TOKEN = "8624963114:AAEvM6LxOwGYE346bOu7gvBgj8f6lZOmjBU"
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=10)

# =========================
# Papkalar
# =========================
DOWNLOAD_FOLDER = "downloads"
DATA_FOLDER = "data"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

USERS_FILE = f"{DATA_FOLDER}/users.json"
STATS_FILE = f"{DATA_FOLDER}/stats.json"

# =========================
# JSON helpers
# =========================
def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return default

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"JSON saqlashda xato: {e}")

# =========================
# Ma'lumotlar yuklash
# =========================
users_db = load_json(USERS_FILE, {})
stats_db = load_json(STATS_FILE, {"total_downloads": 0, "videos": 0, "audios": 0, "searches": 0})

# =========================
# Foydalanuvchi saqlash
# =========================
def register_user(message):
    uid = str(message.from_user.id)
    if uid not in users_db:
        users_db[uid] = {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "joined": datetime.now().isoformat(),
            "downloads": 0
        }
    else:
        users_db[uid]["username"] = message.from_user.username
        users_db[uid]["first_name"] = message.from_user.first_name
    save_json(USERS_FILE, users_db)

def update_stats(type_):
    if type_ == "video":
        stats_db["videos"] += 1
        stats_db["total_downloads"] += 1
    elif type_ == "audio":
        stats_db["audios"] += 1
        stats_db["total_downloads"] += 1
    elif type_ == "search":
        stats_db["searches"] += 1
    save_json(STATS_FILE, stats_db)

# =========================
# URL aniqlash
# =========================
URL_PATTERN = re.compile(
    r'(https?://)?(www\.)?(youtube\.com|youtu\.be|instagram\.com|tiktok\.com|'
    r'vm\.tiktok\.com|facebook\.com|fb\.watch|twitter\.com|x\.com|'
    r'vimeo\.com|dailymotion\.com|soundcloud\.com|pinterest\.com|'
    r'reddit\.com|twitch\.tv|ok\.ru|vk\.com)[\S]+'
)

def is_url(text):
    return bool(URL_PATTERN.search(text.strip()))

def extract_video_id(url):
    match = re.search(r'(?:v=|youtu\.be/|/video/)([a-zA-Z0-9_-]{11})', url)
    return match.group(1) if match else None

# =========================
# Video yuklash
# =========================
def download_video(url):
    opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(id)s_video.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "merge_output_format": "mp4",
        "concurrent_fragment_downloads": 10,
        "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        "socket_timeout": 30,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if not filename.endswith(".mp4"):
            filename = filename.rsplit(".", 1)[0] + ".mp4"
        title = info.get("title", "Video")
    return filename, title

# =========================
# Audio yuklash
# =========================
def download_audio(url):
    opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(id)s_audio.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "concurrent_fragment_downloads": 10,
        "socket_timeout": 30,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        base = ydl.prepare_filename(info)
        filename = base.rsplit(".", 1)[0] + ".mp3"
        title = info.get("title", "Audio")
        artist = info.get("artist") or info.get("uploader", "")
    return filename, title, artist

# =========================
# Qo'shiq qidirish
# =========================
def search_songs(query, max_results=5):
    opts = {
        "quiet": True,
        "noplaylist": True,
        "extract_flat": True,
        "default_search": f"ytsearch{max_results}",
        "socket_timeout": 20,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=False)
        results = []
        for entry in info.get("entries", []):
            results.append({
                "id": entry.get("id"),
                "title": entry.get("title", "Nomsiz"),
                "duration": entry.get("duration"),
                "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                "uploader": entry.get("uploader", ""),
            })
    return results

# =========================
# Fayl tozalash
# =========================
def safe_remove(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except:
        pass

def format_duration(seconds):
    if not seconds:
        return "?"
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"

# =========================
# /start
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    register_user(message)
    uid = message.from_user.id
    text = (
        "🎵 *Salom! Men Pixo Botman!*\n\n"
        "📥 *Nima qila olaman?*\n"
        "• YouTube, Instagram, TikTok, Facebook va boshqalardan video\n"
        "• Videodagi musiqani MP3 formatda\n"
        "• Qo'shiq nomini yozsangiz — topib beraman\n\n"
        "🚀 *Foydalanish:*\n"
        "1️⃣ Video havolasini yuboring\n"
        "2️⃣ Qo'shiq nomini yozing\n\n"
        f"👥 Foydalanuvchilar: *{len(users_db)}*\n"
        f"⬇️ Yuklanmalar: *{stats_db['total_downloads']}*"
    )
    bot.send_message(uid, text, parse_mode="Markdown")

# =========================
# Callback handler
# =========================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    data = call.data
    file_path = None

    if data.startswith("dl_audio:"):
        video_id = data.split(":", 1)[1]
        url = f"https://www.youtube.com/watch?v={video_id}"
        bot.answer_callback_query(call.id, "⏳ Yuklanmoqda...")
        msg = bot.send_message(call.message.chat.id, "⏳ Audio yuklanmoqda... 🎵")
        try:
            file_path, title, artist = download_audio(url)
            with open(file_path, "rb") as f:
                bot.send_audio(
                    call.message.chat.id, f,
                    title=title, performer=artist,
                    caption=f"🎵 *{title}*\n👤 {artist or 'Unknown'}\n\n📤 *Pixo Bot*",
                    parse_mode="Markdown"
                )
            bot.delete_message(call.message.chat.id, msg.message_id)
            update_stats("audio")
            uid_str = str(uid)
            users_db[uid_str]["downloads"] = users_db[uid_str].get("downloads", 0) + 1
            save_json(USERS_FILE, users_db)
        except Exception as e:
            bot.edit_message_text(f"❌ Xato: {str(e)[:150]}", call.message.chat.id, msg.message_id)
        finally:
            safe_remove(file_path)

# =========================
# Video URL handler
# =========================
def handle_video_url(message, url):
    uid = message.from_user.id
    msg = bot.reply_to(message, "⏳ Video yuklanmoqda... 🎬")
    file_path = None
    try:
        file_path, title = download_video(url)
        markup = InlineKeyboardMarkup()
        vid_id = extract_video_id(url)
        if vid_id:
            markup.add(InlineKeyboardButton("🎵 Qo'shiqni yuklab olish", callback_data=f"dl_audio:{vid_id}"))
        with open(file_path, "rb") as video:
            bot.send_video(
                message.chat.id, video,
                caption=f"🎬 *{title}*\n\n📤 *Pixo Bot*",
                supports_streaming=True,
                reply_markup=markup if vid_id else None,
                parse_mode="Markdown"
            )
        bot.delete_message(message.chat.id, msg.message_id)
        update_stats("video")
        uid_str = str(uid)
        users_db[uid_str]["downloads"] = users_db[uid_str].get("downloads", 0) + 1
        save_json(USERS_FILE, users_db)
    except Exception as e:
        logger.error(f"Video yuklashda xato: {e}")
        bot.edit_message_text(f"❌ Xato: {str(e)[:200]}", message.chat.id, msg.message_id)
    finally:
        safe_remove(file_path)

# =========================
# Qo'shiq qidirish handler
# =========================
def handle_song_search(message, query):
    uid = message.from_user.id
    msg = bot.reply_to(message, f"🔍 *{query}* qidirilmoqda...", parse_mode="Markdown")
    try:
        results = search_songs(query, max_results=5)
        if not results:
            bot.edit_message_text("❌ Hech narsa topilmadi.", message.chat.id, msg.message_id)
            return
        markup = InlineKeyboardMarkup(row_width=1)
        text = f"🎵 *{query}* bo'yicha natijalar:\n\n"
        for i, r in enumerate(results, 1):
            dur = format_duration(r["duration"])
            text += f"{i}. *{r['title'][:45]}* — {dur}\n"
            btn = f"{i}. {r['title'][:35]} {dur}"
            markup.add(InlineKeyboardButton(f"🎵 {btn}", callback_data=f"dl_audio:{r['id']}"))
        bot.edit_message_text(text, message.chat.id, msg.message_id,
                              parse_mode="Markdown", reply_markup=markup)
        update_stats("search")
    except Exception as e:
        logger.error(f"Qidirishda xato: {e}")
        bot.edit_message_text(f"❌ Xato: {str(e)[:200]}", message.chat.id, msg.message_id)

# =========================
# Asosiy message handler
# =========================
@bot.message_handler(func=lambda m: True, content_types=["text"])
def main_handler(message):
    register_user(message)
    text = message.text.strip()
    if text.startswith("/"):
        return
    if is_url(text):
        handle_video_url(message, text)
    else:
        handle_song_search(message, text)

# =========================
# Flask Web Service
# =========================
app = Flask(__name__)

@app.route("/")
def index():
    return f"🚀 Pixo Bot ishlayapti! | Foydalanuvchilar: {len(users_db)} | Yuklanmalar: {stats_db['total_downloads']}"

@app.route("/stats")
def web_stats():
    return json.dumps({
        "users": len(users_db),
        "total_downloads": stats_db["total_downloads"],
        "videos": stats_db["videos"],
        "audios": stats_db["audios"],
        "searches": stats_db["searches"]
    }, ensure_ascii=False)

# =========================
# Bot thread
# =========================
def run_bot():
    logger.info("Pixo Bot ishga tushdi!")
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)

bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

# =========================
# Flask
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
