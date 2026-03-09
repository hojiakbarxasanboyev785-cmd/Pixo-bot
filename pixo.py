import telebot
import yt_dlp
import os
import speech_recognition as sr

TOKEN = "8624963114:AAHbnDDhzIDZU23YBzFFpfYquMM_hG6H-Gk"
bot = telebot.TeleBot(TOKEN)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
users = set()

YDL_VIDEO = {
    "format": "bv*+ba/best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
}

YDL_AUDIO = {
    "format": "bestaudio/best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

def download_video(url):
    with yt_dlp.YoutubeDL(YDL_VIDEO) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

def download_music(query):
    with yt_dlp.YoutubeDL(YDL_AUDIO) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=True)
        info = result["entries"][0]
        title = info["title"]
        base = os.path.splitext(ydl.prepare_filename(info))[0]
        filename = base + ".mp3"
    return filename, title

def voice_to_text(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="uz-UZ")

def safe_remove(*paths):
    for p in paths:
        try:
            if p and os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🤖 <b>AI Music & Video Bot</b>\n\n"
        f"🎤 Ovozli xabar — musiqa topamiz\n"
        f"🔎 Matn — musiqa qidiramiz\n"
        f"📥 Link — YouTube/Instagram/TikTok\n\n"
        f"👥 Foydalanuvchilar: <b>{len(users)}</b>",
        parse_mode="HTML",
    )

@bot.message_handler(content_types=["voice"])
def voice_handler(message):
    users.add(message.from_user.id)
    msg = bot.reply_to(message, "🎤 Ovozni aniqlayapman...")
    voice_path = None
    music_path = None
    try:
        file_info = bot.get_file(message.voice.file_id)
        file_bytes = bot.download_file(file_info.file_path)
        voice_path = os.path.join(DOWNLOAD_FOLDER, f"voice_{message.from_user.id}.ogg")
        with open(voice_path, "wb") as f:
            f.write(file_bytes)
        text = voice_to_text(voice_path)
        bot.edit_message_text(f"🔎 Qidiruv: <b>{text}</b>", message.chat.id, msg.message_id, parse_mode="HTML")
        music_path, title = download_music(text)
        with open(music_path, "rb") as a:
            bot.send_audio(message.chat.id, a, title=title, caption=f"🎵 {title}")
    except sr.UnknownValueError:
        bot.edit_message_text("❌ Ovoz aniqlanmadi.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato: {e}", message.chat.id, msg.message_id)
    finally:
        safe_remove(voice_path, music_path)

@bot.message_handler(func=lambda m: True)
def text_handler(message):
    users.add(message.from_user.id)
    text = message.text.strip()
    file_path = None
    if text.startswith("http"):
        msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")
        try:
            file_path, title = download_video(text)
            with open(file_path, "rb") as v:
                bot.send_video(message.chat.id, v, caption=f"🎬 {title}", supports_streaming=True)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xato:\n{e}", message.chat.id, msg.message_id)
        finally:
            safe_remove(file_path)
    else:
        msg = bot.reply_to(message, "🔎 Musiqa qidirilmoqda...")
        try:
            file_path, title = download_music(text)
            with open(file_path, "rb") as a:
                bot.send_audio(message.chat.id, a, title=title, caption=f"🎵 {title}")
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xato:\n{e}", message.chat.id, msg.message_id)
        finally:
            safe_remove(file_path)

print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)
