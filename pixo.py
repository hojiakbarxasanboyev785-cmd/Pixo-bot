import telebot
import yt_dlp
import os
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "8624963114:AAGhw4Ts5ZMkyJK-8YRlxCvVg8xGLFFBDsE"
bot = telebot.TeleBot(TOKEN)

bot.remove_webhook()
time.sleep(2)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

users = set()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        pass

def run_server():
    HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()

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
