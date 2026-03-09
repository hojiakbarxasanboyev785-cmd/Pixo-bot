import telebot
import yt_dlp
import os
import time
import speech_recognition as sr

TOKEN = "8624963114:AAEyVTmF8VKu5WXQrITAWecB97shsWLIGe8"
bot = telebot.TeleBot(TOKEN)

bot.remove_webhook()
time.sleep(2)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

users = set()

# VIDEO YUKLASH
def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")

    return file, title


# MUSIQA YUKLASH
def download_music(query):
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
