import telebot
import yt_dlp
import os

TOKEN = "8624963114:AAHoc7wi89A3PjzWZiNZk5PIO9ymn0NnpD8"
bot = telebot.TeleBot(TOKEN)

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
        'quiet': True,
        'nocheckcertificate': True,
        'concurrent_fragment_downloads': 10,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
            }
        },
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

# MUSIQA QIDIRISH VA YUKLASH
def search_music(query):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
        'nocheckcertificate': True,
        'noplaylist': True,
        'source_address': '0.0.0.0',
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
                'player_skip': ['webpage', 'configs'],
            }
        },
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
        title = info['title']
        file = ydl.prepare_filename(info)
    return file, title

@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"""
🤖 Video & Music Downloader Bot

📥 Video linki yuboring — video yuklaydi
🎵 Musiqa nomini yozing — musiqa yuklaydi

👥 Bot foydalanuvchilari: {len(users)}
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
                    caption=f"🎬 {title}"
                )
            os.remove(file)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.reply_to(message, f"❌ Video yuklab bo'lmadi:\n{e}")

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
            bot.reply_to(message, f"❌ Musiqa topilmadi:\n{e}")

print("Bot ishlayapti...")
bot.infinity_polling()        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
        'nocheckcertificate': True,
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

    bot.send_message(
        message.chat.id,
        f"""
🤖 Video & Music Downloader Bot

📥 Video linki yuboring — video yuklaydi
🎵 Musiqa nomini yozing — MP3 yuklaydi

👥 Bot foydalanuvchilari: {len(users)}
"""
    )

@bot.message_handler(func=lambda m: True)
def handler(message):
    users.add(message.from_user.id)
    text = message.text

    # LINK YUBORILSA — VIDEO QILIB YUBORADI
    if "http" in text:
        msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")

        try:
            file, title = download_video(text)

            with open(file, "rb") as v:
                bot.send_video(
                    message.chat.id,
                    v,
                    caption=f"🎬 {title}"
                )

            os.remove(file)
            bot.delete_message(message.chat.id, msg.message_id)

        except Exception as e:
            bot.reply_to(message, f"❌ Video yuklab bo'lmadi: {e}")

    # MATN YOZILSA — MUSIQA QIDIRIB YUBORADI
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
            bot.reply_to(message, f"❌ Musiqa topilmadi: {e}")

print("Bot ishlayapti...")
bot.infinity_polling()
