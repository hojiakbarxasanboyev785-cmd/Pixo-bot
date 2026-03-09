import telebot
import yt_dlp
import os
import re

TOKEN = "8624963114:AAEvM6LxOwGYE346bOu7gvBgj8f6lZOmjBU"
bot = telebot.TeleBot(TOKEN)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

users = set()

# Platformani aniqlash
def detect_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "instagram.com" in url:
        return "instagram"
    elif "facebook.com" in url or "fb.watch" in url:
        return "facebook"
    elif "tiktok.com" in url:
        return "tiktok"
    else:
        return "unknown"

# VIDEO YUKLASH
def download_video(url):
    platform = detect_platform(url)
    
    # Asosiy sozlamalar
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s_%(id)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'concurrent_fragment_downloads': 10,
    }
    
    # Platformaga qarab qo'shimcha sozlamalar
    if platform == "instagram":
        ydl_opts['format'] = 'best'
        ydl_opts['extract_flat'] = False
    elif platform == "tiktok":
        ydl_opts['format'] = 'best'
        ydl_opts['extractor_args'] = {'tiktok': {'webpage_download': True}}
    elif platform == "facebook":
        ydl_opts['format'] = 'best'
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # URL ni tozalash
            info = ydl.extract_info(url, download=True)
            
            # Yuklangan fayl nomini topish
            if 'entries' in info:
                # Playlist bo'lsa birinchi videoni olish
                info = info['entries'][0]
            
            # Fayl nomini to'g'ri olish
            filename = ydl.prepare_filename(info)
            
            # Agar kengaytma yo'q bo'lsa qo'shish
            if not os.path.exists(filename):
                filename = filename.replace('.webm', '.mp4').replace('.mkv', '.mp4')
            
            title = info.get("title", "Video")
            
            return filename, title, platform
        except Exception as e:
            raise Exception(f"{platform} dan yuklashda xatolik: {str(e)}")

@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.from_user.id)
    
    # Foydalanuvchi ismini olish
    user_name = message.from_user.first_name
    
    bot.send_message(
        message.chat.id,
        f"👋 Salom, {user_name} Men Pixo botman!\n\n"
        f"📥 Menga quyidagi platformalardan video link yuboring:\n"
        f"• YouTube\n"
        f"• Instagram\n"
        f"• Facebook\n"
        f"• TikTok\n\n"
        f"Men avtomatik tarzda videoni yuklab beraman!\n\n"
        f"👥 Bot foydalanuvchilari: {len(users)}"
    )

@bot.message_handler(func=lambda m: True)
def handle_video(message):
    users.add(message.from_user.id)
    url = message.text.strip()
    
    # Linkni tekshirish
    if not re.match(r'https?://', url):
        bot.reply_to(message, "❌ Iltimos, to'g'ri video link yuboring!")
        return
    
    # Platformani aniqlash
    platform = detect_platform(url)
    
    if platform == "unknown":
        bot.reply_to(message, "❌ Faqat YouTube, Instagram, Facebook va TikTok dan video yuklay olaman!")
        return
    
    # Yuklash boshlanishi
    msg = bot.reply_to(message, f"⏳ {platform.capitalize()} dan video yuklanmoqda...\nBu biroz vaqt olishi mumkin.")
    
    try:
        file, title, platform = download_video(url)
        
        # Fayl borligini tekshirish
        if not os.path.exists(file):
            # Muqobil nomlarni qidirish
            files = os.listdir(DOWNLOAD_FOLDER)
            video_files = [f for f in files if f.endswith(('.mp4', '.mkv', '.webm'))]
            if video_files:
                # Eng oxirgi yuklangan faylni olish
                file = os.path.join(DOWNLOAD_FOLDER, sorted(video_files, key=lambda x: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, x)))[-1])
            else:
                raise Exception("Video fayl topilmadi")
        
        # Videoni yuborish
        with open(file, "rb") as v:
            bot.send_video(
                message.chat.id,
                v,
                caption=f"✅ {platform.capitalize()} | {title[:50]}...",
                timeout=60
            )
        
        # Faylni o'chirish
        os.remove(file)
        
        # Yuklash xabarini o'chirish
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        error_text = str(e)
        bot.reply_to(message, f"❌ Video yuklab bo'lmadi!\nXatolik: {error_text[:200]}")
        
        # Xatolik yuz berganda fayllarni tozalash
        try:
            if 'file' in locals() and os.path.exists(file):
                os.remove(file)
        except:
            pass

@bot.message_handler(commands=['stats'])
def stats(message):
    bot.reply_to(message, f"📊 Bot statistikasi:\n\n👥 Foydalanuvchilar: {len(users)}")

print("🤖 Bot ishga tushdi...")
print("📱 Qo'llab-quvvatlanadigan platformalar: YouTube, Instagram, Facebook, TikTok")
bot.infinity_polling()
