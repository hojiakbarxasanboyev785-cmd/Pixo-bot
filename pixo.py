import os
import re
import json
import threading
import logging
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import yt_dlp
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, jsonify

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

# =========================
# JSON helpers
# =========================
def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"JSON load error: {e}")
    return default

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"JSON save error: {e}")

# =========================
# Foydalanuvchi bazasi
# =========================
users_db = load_json(USERS_FILE, {})

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

# =========================
# URL aniqlash
# =========================
URL_PATTERN = re.compile(
    r'(https?://)?(www\.)?(youtube\.com|youtu\.be|instagram\.com|tiktok\.com|vm\.tiktok\.com)[\S]+'
)

def is_url(text):
    return bool(URL_PATTERN.search(text.strip()))

def extract_video_id(url):
    parsed = urlparse(url)
    if "youtu.be" in parsed.netloc:
        return parsed.path[1:]
    elif "youtube.com" in parsed.netloc:
        if "/shorts/" in parsed.path:
            return parsed.path.split("/shorts/")[1]
        qs = parse_qs(parsed.query)
        return qs.get("v", [None])[0]
    return None

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
        "http_headers": {"User-Agent": "Mozilla/5.0"},
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
        filename = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"
        title = info.get("title", "Audio")
        artist = info.get("uploader", "")
    return filename, title, artist

# =========================
# Qo‘shiq qidirish
# =========================
def search_songs(query, max_results=5):
    opts = {
        "quiet": True,
        "noplaylist": True,
        "extract_flat": True,
        "default_search": f"ytsearch{max_results}:youtube",
        "force_generic_extractor": True,
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
# Faylni tozalash
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
        "📥 Video URL yuboring yoki qo'shiq nomini yozing.\n"
        f"👥 Foydalanuvchilar: *{len(users_db)}*"
    )
    bot.send_message(uid, text, parse_mode="Markdown")

# =========================
# Callback handler (audio yuklash)
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
                    caption=f"🎵 *{title}*\n👤 {artist or 'Unknown'}",
                    parse_mode="Markdown"
                )
            bot.delete_message(call.message.chat.id, msg.message_id)
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
            markup.add(InlineKeyboardButton("🎵 Audio yuklab olish", callback_data=f"dl_audio:{vid_id}"))
        with open(file_path, "rb") as video:
            bot.send_video(
                message.chat.id, video,
                caption=f"🎬 *{title}*",
                supports_streaming=True,
                reply_markup=markup if vid_id else None,
                parse_mode="Markdown"
            )
        bot.delete_message(message.chat.id, msg.message_id)
        uid_str = str(uid)
        users_db[uid_str]["downloads"] = users_db[uid_str].get("downloads", 0) + 1
        save_json(USERS_FILE, users_db)
    except Exception as e:
        logger.error(f"Video yuklash xato: {e}")
        bot.edit_message_text(f"❌ Xato: {str(e)[:200]}", message.chat.id, msg.message_id)
    finally:
        safe_remove(file_path)

# =========================
# Qo‘shiq qidirish handler
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
            markup.add(InlineKeyboardButton(f"🎵 {r['title'][:35]} {dur}", callback_data=f"dl_audio:{r['id']}"))
        bot.edit_message_text(text, message.chat.id, msg.message_id,
                              parse_mode="Markdown", reply_markup=markup)
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
    return f"🚀 Pixo Bot ishlayapti! | Foydalanuvchilar: {len(users_db)}"

# =========================
# Bot thread
# =========================
def run_bot():
    logger.info("Pixo Bot ishga tushdi!")
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)

bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

# =========================
# Flask run
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
