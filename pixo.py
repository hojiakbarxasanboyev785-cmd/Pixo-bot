import telebot
import yt_dlp
import os
import time

TOKEN = "8624963114:AAGhw4Ts5ZMkyJK-8YRlxCvVg8xGLFFBDsE"
bot = telebot.TeleBot(TOKEN)

bot.remove_webhook()
time.sleep(2)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

users = set()

def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return file, title

def search_music(query):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
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
    )

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
