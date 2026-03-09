import telebot
import yt_dlp
import os
import speech_recognition as sr

# ----------------------------
# BOT TOKEN
TOKEN = "8624963114:AAHbnDDhzIDZU23YBzFFpfYquMM_hG6H-Gk"  # ⚠️ Tokeningizni bu yerga yozing
bot = telebot.TeleBot(TOKEN)

# ----------------------------
# DOWNLOAD papkasi
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

users = set()

# ----------------------------
# Video yuklash konfiguratsiyasi
YDL_VIDEO = {
    "format": "bv*+ba/best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
    "concurrent_fragment_downloads": 5,
    "nocheckcertificate": True,
}

# Audio yuklash konfiguratsiyasi
YDL_AUDIO = {
    "format": "bestaudio/best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
    "quiet": True,
    "noplaylist": True,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

# ----------------------------
# VIDEO YUKLASH
def download_video(url):
    with yt_dlp.YoutubeDL(YDL_VIDEO) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

# ----------------------------
# MUSIQA YUKLASH
def download_music(query):
    with yt_dlp.YoutubeDL(YDL_AUDIO) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=True)
        info = result["entries"][0]
        title = info["title"]
        # yt-dlp postprocessor mp3 ga o'zgartiradi
        base = os.path.splitext(ydl.prepare_filename(info))[0]
        filename = base + ".mp3"
    return filename, title

# ----------------------------
# OVOZ → MATN
def voice_to_text(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="uz-UZ")

# ----------------------------
# Faylni xavfsiz o'chirish
def safe_remove(*paths):
    for p in paths:
        try:
            if p and os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

# ----------------------------
# /start
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🤖 <b>AI Music & Video Bot</b>\n\n"
        f"🎤 Ovozli xabar yuboring — musiqa topamiz\n"
        f"🔎 Matn yuboring — musiqa qidiramiz\n"
        f"📥 Link yuboring — YouTube / Instagram / TikTok / Facebook\n\n"
        f"👥 Foydalanuvchilar: <b>{len(users)}</b>",
        parse_mode="HTML",
    )

# ----------------------------
# OVOZLI XABAR
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
        bot.edit_message_text("❌ Ovoz aniqlanmadi. Qaytadan yuboring.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato: {e}", message.chat.id, msg.message_id)
    finally:
        safe_remove(voice_path, music_path)

# ----------------------------
# MATN / LINK HANDLER
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
                bot.send_video(
                    message.chat.id, v,
                    caption=f"🎬 {title}",
                    supports_streaming=True,
                )
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
                bot.send_audio(
                    message.chat.id, a,
                    title=title,
                    caption=f"🎵 {title}",
                )
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xato:\n{e}", message.chat.id, msg.message_id)
        finally:
            safe_remove(file_path)

# ----------------------------
print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

# ----------------------------
# VIDEO YUKLASH
def download_video(url):
    with yt_dlp.YoutubeDL(YDL_VIDEO) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

# ----------------------------
# MUSIQA YUKLASH
def download_music(query):
    with yt_dlp.YoutubeDL(YDL_AUDIO) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=True)
        info = result["entries"][0]
        title = info["title"]
        base = os.path.splitext(ydl.prepare_filename(info))[0]
        filename = base + ".mp3"
    return filename, title

# ----------------------------
# OVOZ → MATN
def voice_to_text(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="uz-UZ")

# ----------------------------
# Faylni xavfsiz o'chirish
def safe_remove(*paths):
    for p in paths:
        try:
            if p and os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

# ----------------------------
# /start
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🤖 <b>AI Music & Video Bot</b>\n\n"
        f"🎤 Ovozli xabar yuboring — musiqa topamiz\n"
        f"🔎 Matn yuboring — musiqa qidiramiz\n"
        f"📥 Link yuboring — YouTube / Instagram / TikTok / Facebook\n\n"
        f"👥 Foydalanuvchilar: <b>{len(users)}</b>",
        parse_mode="HTML",
    )

# ----------------------------
# OVOZLI XABAR
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
        bot.edit_message_text("❌ Ovoz aniqlanmadi. Qaytadan yuboring.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato: {e}", message.chat.id, msg.message_id)
    finally:
        safe_remove(voice_path, music_path)

# ----------------------------
# MATN / LINK HANDLER
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
                bot.send_video(
                    message.chat.id, v,
                    caption=f"🎬 {title}",
                    supports_streaming=True,
                )
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
                bot.send_audio(
                    message.chat.id, a,
                    title=title,
                    caption=f"🎵 {title}",
                )
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xato:\n{e}", message.chat.id, msg.message_id)
        finally:
            safe_remove(file_path)

# ----------------------------
print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

# ----------------------------
# VIDEO YUKLASH
def download_video(url):
    with yt_dlp.YoutubeDL(YDL_VIDEO) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

# ----------------------------
# MUSIQA YUKLASH
def download_music(query):
    with yt_dlp.YoutubeDL(YDL_AUDIO) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=True)
        info = result["entries"][0]
        title = info["title"]
        base = os.path.splitext(ydl.prepare_filename(info))[0]
        filename = base + ".mp3"
    return filename, title

# ----------------------------
# OVOZ → MATN
def voice_to_text(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="uz-UZ")

# ----------------------------
# Faylni xavfsiz o'chirish
def safe_remove(*paths):
    for p in paths:
        try:
            if p and os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

# ----------------------------
# /start
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🤖 <b>AI Music & Video Bot</b>\n\n"
        f"🎤 Ovozli xabar yuboring — musiqa topamiz\n"
        f"🔎 Matn yuboring — musiqa qidiramiz\n"
        f"📥 Link yuboring — YouTube / Instagram / TikTok / Facebook\n\n"
        f"👥 Foydalanuvchilar: <b>{len(users)}</b>",
        parse_mode="HTML",
    )

# ----------------------------
# OVOZLI XABAR
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
        bot.edit_message_text("❌ Ovoz aniqlanmadi. Qaytadan yuboring.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato: {e}", message.chat.id, msg.message_id)
    finally:
        safe_remove(voice_path, music_path)

# ----------------------------
# MATN / LINK HANDLER
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
                bot.send_video(
                    message.chat.id, v,
                    caption=f"🎬 {title}",
                    supports_streaming=True,
                )
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
                bot.send_audio(
                    message.chat.id, a,
                    title=title,
                    caption=f"🎵 {title}",
                )
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xato:\n{e}", message.chat.id, msg.message_id)
        finally:
            safe_remove(file_path)

# ----------------------------
print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

# ----------------------------
# VIDEO YUKLASH
def download_video(url):
    with yt_dlp.YoutubeDL(YDL_VIDEO) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

# ----------------------------
# MUSIQA YUKLASH
def download_music(query):
    with yt_dlp.YoutubeDL(YDL_AUDIO) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=True)
        info = result["entries"][0]
        title = info["title"]
        base = os.path.splitext(ydl.prepare_filename(info))[0]
        filename = base + ".mp3"
    return filename, title

# ----------------------------
# OVOZ → MATN
def voice_to_text(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="uz-UZ")

# ----------------------------
# Faylni xavfsiz o'chirish
def safe_remove(*paths):
    for p in paths:
        try:
            if p and os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

# ----------------------------
# /start
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🤖 <b>AI Music & Video Bot</b>\n\n"
        f"🎤 Ovozli xabar yuboring — musiqa topamiz\n"
        f"🔎 Matn yuboring — musiqa qidiramiz\n"
        f"📥 Link yuboring — YouTube / Instagram / TikTok / Facebook\n\n"
        f"👥 Foydalanuvchilar: <b>{len(users)}</b>",
        parse_mode="HTML",
    )

# ----------------------------
# OVOZLI XABAR
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
        bot.edit_message_text("❌ Ovoz aniqlanmadi. Qaytadan yuboring.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato: {e}", message.chat.id, msg.message_id)
    finally:
        safe_remove(voice_path, music_path)

# ----------------------------
# MATN / LINK HANDLER
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
                bot.send_video(
                    message.chat.id, v,
                    caption=f"🎬 {title}",
                    supports_streaming=True,
                )
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
                bot.send_audio(
                    message.chat.id, a,
                    title=title,
                    caption=f"🎵 {title}",
                )
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xato:\n{e}", message.chat.id, msg.message_id)
        finally:
            safe_remove(file_path)

# ----------------------------
print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

# ----------------------------
# VIDEO YUKLASH
def download_video(url):
    with yt_dlp.YoutubeDL(YDL_VIDEO) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

# ----------------------------
# MUSIQA YUKLASH
def download_music(query):
    with yt_dlp.YoutubeDL(YDL_AUDIO) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=True)
        info = result["entries"][0]
        title = info["title"]
        base = os.path.splitext(ydl.prepare_filename(info))[0]
        filename = base + ".mp3"
    return filename, title

# ----------------------------
# OVOZ → MATN
def voice_to_text(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="uz-UZ")

# ----------------------------
# Faylni xavfsiz o'chirish
def safe_remove(*paths):
    for p in paths:
        try:
            if p and os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

# ----------------------------
# /start
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🤖 <b>AI Music & Video Bot</b>\n\n"
        f"🎤 Ovozli xabar yuboring — musiqa topamiz\n"
        f"🔎 Matn yuboring — musiqa qidiramiz\n"
        f"📥 Link yuboring — YouTube / Instagram / TikTok / Facebook\n\n"
        f"👥 Foydalanuvchilar: <b>{len(users)}</b>",
        parse_mode="HTML",
    )

# ----------------------------
# OVOZLI XABAR
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
        bot.edit_message_text("❌ Ovoz aniqlanmadi. Qaytadan yuboring.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato: {e}", message.chat.id, msg.message_id)
    finally:
        safe_remove(voice_path, music_path)

# ----------------------------
# MATN / LINK HANDLER
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
                bot.send_video(
                    message.chat.id, v,
                    caption=f"🎬 {title}",
                    supports_streaming=True,
                )
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
                bot.send_audio(
                    message.chat.id, a,
                    title=title,
                    caption=f"🎵 {title}",
                )
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xato:\n{e}", message.chat.id, msg.message_id)
        finally:
            safe_remove(file_path)

# ----------------------------
print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}


# ----------------------------
# VIDEO YUKLASH
def download_video(url):
    with yt_dlp.YoutubeDL(YDL_VIDEO) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title


# ----------------------------
# MUSIQA YUKLASH
def download_music(query):
    with yt_dlp.YoutubeDL(YDL_AUDIO) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=True)
        info = result["entries"][0]
        title = info["title"]
        # yt-dlp postprocessor mp3 ga o'zgartiradi
        base = os.path.splitext(ydl.prepare_filename(info))[0]
        filename = base + ".mp3"
    return filename, title


# ----------------------------
# OVOZ → MATN
def voice_to_text(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="uz-UZ")


# ----------------------------
# Faylni xavfsiz o'chirish
def safe_remove(*paths):
    for p in paths:
        try:
            if p and os.path.exists(p):
                os.remove(p)
        except Exception:
            pass


# ----------------------------
# /start
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🤖 <b>AI Music & Video Bot</b>\n\n"
        f"🎤 Ovozli xabar yuboring — musiqa topamiz\n"
        f"🔎 Matn yuboring — musiqa qidiramiz\n"
        f"📥 Link yuboring — YouTube / Instagram / TikTok / Facebook\n\n"
        f"👥 Foydalanuvchilar: <b>{len(users)}</b>",
        parse_mode="HTML",
    )


# ----------------------------
# OVOZLI XABAR
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
        bot.edit_message_text("❌ Ovoz aniqlanmadi. Qaytadan yuboring.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato: {e}", message.chat.id, msg.message_id)
    finally:
        safe_remove(voice_path, music_path)


# ----------------------------
# MATN / LINK HANDLER
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
                bot.send_video(
                    message.chat.id, v,
                    caption=f"🎬 {title}",
                    supports_streaming=True,
                )
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
                bot.send_audio(
                    message.chat.id, a,
                    title=title,
                    caption=f"🎵 {title}",
                )
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Xato:\n{e}", message.chat.id, msg.message_id)
        finally:
            safe_remove(file_path)


# ----------------------------
print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)    with yt_dlp.YoutubeDL(YDL_VIDEO) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

def download_music(query):
    with yt_dlp.YoutubeDL(YDL_AUDIO) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)["entries"][0]
        title = info["title"]
        filename = f"{DOWNLOAD_FOLDER}/{title}.mp3"
    return filename, title

def voice_to_text(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    text = r.recognize_google(audio)
    return text

@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🤖 AI Music & Video Bot\n\n"
        f"🎤 Mikrofon bilan musiqa ayting\n"
        f"🎵 Bot MP3 topadi\n\n"
        f"📥 Link yuboring: YouTube, Instagram, TikTok\n"
        f"👥 Users: {len(users)}"
    )

@bot.message_handler(content_types=["voice"])
def voice_handler(message):
    msg = bot.reply_to(message, "🎤 Ovozni aniqlayapman...")
    file_info = bot.get_file(message.voice.file_id)
    file = bot.download_file(file_info.file_path)
    voice_path = f"{DOWNLOAD_FOLDER}/voice.ogg"
    with open(voice_path, "wb") as f:
        f.write(file)
    try:
        text = voice_to_text(voice_path)
        bot.send_message(message.chat.id, f"🔎 Qidiruv: {text}")
        music, title = download_music(text)
        with open(music, "rb") as a:
            bot.send_audio(message.chat.id, a, title=title)
        os.remove(music)
        os.remove(voice_path)
    except Exception as e:
        bot.reply_to(message, f"❌ Xato: {e}")

@bot.message_handler(func=lambda m: True)
def handler(message):
    users.add(message.from_user.id)
    text = message.text
    if "http" in text:
        msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")
        try:
            video, title = download_video(text)
            with open(video, "rb") as v:
                bot.send_video(message.chat.id, v, caption=f"🎬 {title}", supports_streaming=True)
            os.remove(video)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.reply_to(message, f"❌ Xato:\n{e}")
    else:
        msg = bot.reply_to(message, "🔎 Musiqa qidirilmoqda...")
        try:
            music, title = download_music(text)
            with open(music, "rb") as a:
                bot.send_audio(message.chat.id, a, title=title, caption=f"🎵 {title}")
            os.remove(music)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.reply_to(message, f"❌ Xato:\n{e}")

print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)        "preferredquality": "192"
    }]
}

# -------------------
# VIDEO FUNKSIYA
def download_video(url):
    with yt_dlp.YoutubeDL(YDL_VIDEO) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

# -------------------
# MUSIQA FUNKSIYA
def download_music(query):
    with yt_dlp.YoutubeDL(YDL_AUDIO) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)["entries"][0]
        title = info["title"]
        filename = f"{DOWNLOAD_FOLDER}/{title}.mp3"
    return filename, title

# -------------------
# VOICE → TEXT
def voice_to_text(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    text = r.recognize_google(audio)
    return text

# -------------------
# /start
@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"""🤖 AI Music & Video Bot

🎤 Mikrofon bilan musiqa nomini ayting
🎵 Bot MP3 topadi

📥 Link yuboring:
YouTube
Instagram
TikTok
Facebook

👥 Users: {len(users)}
"""
    )

# -------------------
# VOICE HANDLER
@bot.message_handler(content_types=["voice"])
def voice_handler(message):
    msg = bot.reply_to(message, "🎤 Ovozni aniqlayapman...")

    file_info = bot.get_file(message.voice.file_id)
    file = bot.download_file(file_info.file_path)

    voice_path = f"{DOWNLOAD_FOLDER}/voice.ogg"
    with open(voice_path, "wb") as f:
        f.write(file)

    try:
        text = voice_to_text(voice_path)
        bot.send_message(message.chat.id, f"🔎 Qidiruv: {text}")

        music, title = download_music(text)
        with open(music, "rb") as a:
            bot.send_audio(message.chat.id, a, title=title)

        os.remove(music)
        os.remove(voice_path)

    except Exception as e:
        bot.reply_to(message, f"❌ Xato: {e}")

# -------------------
# TEXT HANDLER
@bot.message_handler(func=lambda m: True)
def handler(message):
    users.add(message.from_user.id)
    text = message.text

    if "http" in text:  # Video
        msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")
        try:
            video, title = download_video(text)
            with open(video, "rb") as v:
                bot.send_video(
                    message.chat.id,
                    v,
                    caption=f"🎬 {title}",
                    supports_streaming=True
                )
            os.remove(video)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.reply_to(message, f"❌ Xato: {e}")

    else:  # Musiqa
        msg = bot.reply_to(message, "🔎 Musiqa qidirilmoqda...")
        try:
            music, title = download_music(text)
            with open(music, "rb") as a:
                bot.send_audio(
                    message.chat.id,
                    a,
                    title=title,
                    caption=f"🎵 {title}"
                )
            os.remove(music)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.reply_to(message, f"❌ Xato: {e}")

# -------------------
print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)    }]
}

# VIDEO YUKLASH
def download_video(url):

    with yt_dlp.YoutubeDL(YDL_VIDEO) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")

    return file, title


# MUSIQA QIDIRISH
def download_music(query):

    with yt_dlp.YoutubeDL(YDL_AUDIO) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)["entries"][0]
        title = info["title"]
        filename = f"{DOWNLOAD_FOLDER}/{title}.mp3"

    return filename, title


# VOICE → TEXT
def voice_to_text(path):

    r = sr.Recognizer()

    with sr.AudioFile(path) as source:
        audio = r.record(source)

    text = r.recognize_google(audio)
    return text


@bot.message_handler(commands=["start"])
def start(message):

    users.add(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"""🤖 AI Music & Video Bot

🎤 Mikrofon bilan musiqa nomini ayting
🎵 Bot MP3 topadi

📥 Link yuboring:
YouTube
Instagram
TikTok
Facebook

👥 Users: {len(users)}
"""
    )


# 🎤 VOICE MESSAGE
@bot.message_handler(content_types=["voice"])
def voice_handler(message):

    msg = bot.reply_to(message, "🎤 Ovozni aniqlayapman...")

    file_info = bot.get_file(message.voice.file_id)
    file = bot.download_file(file_info.file_path)

    voice_path = f"{DOWNLOAD_FOLDER}/voice.ogg"

    with open(voice_path, "wb") as f:
        f.write(file)

    try:

        text = voice_to_text(voice_path)

        bot.send_message(message.chat.id, f"🔎 Qidiruv: {text}")

        music, title = download_music(text)

        with open(music, "rb") as a:
            bot.send_audio(message.chat.id, a, title=title)

        os.remove(music)
        os.remove(voice_path)

    except Exception as e:
        bot.reply_to(message, f"❌ Xato: {e}")


# 📩 TEXT MESSAGE
@bot.message_handler(func=lambda m: True)
def handler(message):

    users.add(message.from_user.id)
    text = message.text

    if "http" in text:

        msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")

        try:

            video, title = download_video(text)

            with open(video, "rb") as v:
                bot.send_video(
                    message.chat.id,
                    v,
                    caption=f"🎬 {title}",
                    supports_streaming=True
                )

            os.remove(video)

        except Exception as e:
            bot.reply_to(message, f"❌ Xato:\n{e}")

    else:

        msg = bot.reply_to(message, "🔎 Musiqa qidirilmoqda...")

        try:

            music, title = download_music(text)

            with open(music, "rb") as a:
                bot.send_audio(message.chat.id, a, title=title)

            os.remove(music)

        except Exception as e:
            bot.reply_to(message, f"❌ Xato:\n{e}")


print("🚀 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)def download_music(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)['entries'][0]
        title = info['title']
        file = f"{DOWNLOAD_FOLDER}/{title}.mp3"

    return file, title


# VOICE → TEXT
def voice_to_text(file_path):

    r = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio = r.record(source)

    text = r.recognize_google(audio)
    return text


@bot.message_handler(commands=['start'])
def start(message):

    users.add(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"""
🤖 AI Music & Video Bot

🎤 Mikrofon bilan musiqa nomini ayting
🎵 Bot musiqani topadi

📥 Link yuboring:
YouTube
Instagram
TikTok

👥 Users: {len(users)}
"""
    )


# VOICE MESSAGE
@bot.message_handler(content_types=['voice'])
def voice_handler(message):

    msg = bot.reply_to(message, "🎤 Ovozni aniqlayapman...")

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    voice_path = f"{DOWNLOAD_FOLDER}/voice.ogg"

    with open(voice_path, 'wb') as f:
        f.write(downloaded_file)

    try:

        text = voice_to_text(voice_path)

        bot.send_message(message.chat.id, f"🔎 Qidiruv: {text}")

        file, title = download_music(text)

        with open(file, "rb") as a:
            bot.send_audio(message.chat.id, a, title=title)

        os.remove(file)
        os.remove(voice_path)

    except Exception as e:
        bot.reply_to(message, f"❌ Xato: {e}")


# TEXT MESSAGE
@bot.message_handler(func=lambda m: True)
def handler(message):

    text = message.text

    if "http" in text:

        msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")

        try:

            file, title = download_video(text)

            with open(file, "rb") as v:
                bot.send_video(message.chat.id, v, caption=title)

            os.remove(file)

        except Exception as e:
            bot.reply_to(message, f"❌ Xato: {e}")

    else:

        msg = bot.reply_to(message, "🔎 Musiqa qidirilmoqda...")

        try:

            file, title = download_music(text)

            with open(file, "rb") as a:
                bot.send_audio(message.chat.id, a, title=title)

            os.remove(file)

        except Exception as e:
            bot.reply_to(message, f"❌ Xato: {e}")


print("🚀 Bot ishga tushdi")
bot.infinity_polling(skip_pending=True)def download_music(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)['entries'][0]
        title = info['title']
        filename = f"{DOWNLOAD_FOLDER}/{title}.mp3"

    return filename, title


@bot.message_handler(commands=['start'])
def start(message):

    users.add(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"""
🤖 Universal Downloader Bot

📥 Link yuboring:
YouTube
Instagram
TikTok
Facebook

🎵 Musiqa nomini yozing — MP3 yuklaydi

👥 Foydalanuvchilar: {len(users)}
"""
    )


@bot.message_handler(func=lambda m: True)
def handler(message):

    users.add(message.from_user.id)
    text = message.text

    # VIDEO
    if "http" in text:

        msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")

        try:

            file, title = download_video(text)

            with open(file, "rb") as v:
                bot.send_video(
                    message.chat.id,
                    v,
                    caption=f"🎬 {title}",
                    supports_streaming=True
                )

            os.remove(file)
            bot.delete_message(message.chat.id, msg.message_id)

        except Exception as e:

            bot.reply_to(message, f"❌ Xato:\n{e}")

    # MUSIQA
    else:

        msg = bot.reply_to(message, "🔎 Musiqa qidirilmoqda...")

        try:

            file, title = download_music(text)

            with open(file, "rb") as a:
                bot.send_audio(
                    message.chat.id,
                    a,
                    title=title,
                    caption=f"🎵 {title}"
                )

            os.remove(file)
            bot.delete_message(message.chat.id, msg.message_id)

        except Exception as e:

            bot.reply_to(message, f"❌ Xato:\n{e}")


print("✅ Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
        file = ydl.prepare_filename(info)
        title = info['title']

    return file, title


@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"""🤖 Universal Downloader Bot

📥 Video link yuboring:
YouTube
Instagram
TikTok
Facebook

🎵 Musiqa nomini yozing — YouTube dan topadi

👥 Foydalanuvchilar: {len(users)}
"""
    )


@bot.message_handler(func=lambda m: True)
def handler(message):
    users.add(message.from_user.id)
    text = message.text

    if "http" in text:
        msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")

        try:
            file, title = download_video(text)

            with open(file, "rb") as v:
                bot.send_video(
                    message.chat.id,
                    v,
                    caption=f"🎬 {title}",
                    supports_streaming=True
                )

            os.remove(file)
            bot.delete_message(message.chat.id, msg.message_id)

        except Exception as e:
            bot.reply_to(message, f"❌ Xato:\n{e}")

    else:
        msg = bot.reply_to(message, "🔎 Musiqa qidirilmoqda...")

        try:
            file, title = search_music(text)

            with open(file, "rb") as a:
                bot.send_audio(
                    message.chat.id,
                    a,
                    title=title,
                    caption=f"🎵 {title}"
                )

            os.remove(file)
            bot.delete_message(message.chat.id, msg.message_id)

        except Exception as e:
            bot.reply_to(message, f"❌ Xato:\n{e}")


print("✅ Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)        'nocheckcertificate': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
        title = info['title']
        file = ydl.prepare_filename(info)
    return file, title

@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(message.chat.id, f"""
🤖 Video & Music Downloader Bot

📥 Video linki yuboring — video yuklaydi
🎵 Musiqa nomini yozing — musiqa yuklaydi

👥 Foydalanuvchilar: {len(users)}
""")

@bot.message_handler(func=lambda m: True)
def handler(message):
    users.add(message.from_user.id)
    text = message.text

    if "http" in text:
        msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")
        try:
            file, title = download_video(text)
            with open(file, "rb") as v:
                bot.send_video(message.chat.id, v, caption=f"🎬 {title}")
            os.remove(file)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.reply_to(message, f"❌ Xato:\n{e}")
    else:
        msg = bot.reply_to(message, "🔎 Musiqa qidirilmoqda...")
        try:
            file, title = search_music(text)
            with open(file, "rb") as a:
                bot.send_audio(message.chat.id, a, title=title, caption=f"🎵 {title}")
            os.remove(file)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.reply_to(message, f"❌ Xato:\n{e}")

print("Bot ishlayapti...")
bot.infinity_polling(skip_pending=True)        "👥 Foydalanuvchilar: " + str(len(users))

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    users.add(message.from_user.id)
    url = message.text
    
    if 'http' not in url:
        bot.reply_to(message, "❌ Iltimos, video link yuboring!")
        return
    
    msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")
    
    try:
        # Video yuklash
        filename, title = download_video(url)
        
        # Videoni yuborish
        with open(filename, 'rb') as video:
            bot.send_video(
                message.chat.id, 
                video, 
                caption=f"🎬 {title}",
                timeout=100
            )
        
        # Faylni o'chirish
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(
            f"❌ Xatolik: {str(e)[:100]}", 
            message.chat.id, 
            msg.message_id
        )

print("✅ Bot ishga tushdi...")
print("👨‍💻 @username - admin")
bot.infinity_polling()    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(message.chat.id,
        "🎬 Video Downloader Bot\n\n"
        "📥 Video linkini yuboring\n\n"
        "Qo'llab-quvvatlanadi: YouTube, Instagram, TikTok, Facebook va boshqalar\n\n"
        "👥 Foydalanuvchilar: " + str(len(users))
    )

@bot.message_handler(func=lambda m: True)
def handler(message):
    users.add(message.from_user.id)
    text = message.text

    if "http" in text:
        msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")
        try:
            file, title = download_video(text)
            with open(file, "rb") as v:
                bot.send_video(message.chat.id, v, caption="🎬 " + title, supports_streaming=True)
            os.remove(file)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.reply_to(message, "❌ Xato: " + str(e))
    else:
        bot.reply_to(message, "❌ Iltimos, video link yuboring!\n\nMasalan: https://youtube.com/watch?v=...")

Thread(target=run_server, daemon=True).start()
print("Bot ishlayapti - faqat video yuklaydi...")
bot.infinity_polling(skip_pending=True)
