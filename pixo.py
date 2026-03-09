import telebot
import yt_dlp
import os

TOKEN = "8624963114:AAGR01L6bgJdKGPYTnSHuH7Z65JgxzDCwj0"  # BotFather dan olingan token
bot = telebot.TeleBot(TOKEN)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

users = set()  # foydalanuvchilarni saqlash

ydl_opts = {
    "format": "best",
    "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
}


def download_video(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        title = info.get("title", "Video")
    return filename, title


def safe_remove(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except:
        pass


@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)  # foydalanuvchini qo‘shish
    bot.send_message(
        message.chat.id,
        f"Salom, men Pixo video yuklovchi botman!\n"
        f"Foydalanuvchilar soni: {len(users)}"
    )


@bot.message_handler(func=lambda m: True)
def handler(message):
    url = message.text.strip()
    users.add(message.from_user.id)

    msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")
    file_path = None

    try:
        file_path, title = download_video(url)
        with open(file_path, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                caption=title,
                supports_streaming=True
            )
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(
            f"❌ Xato:\n{e}",
            message.chat.id,
            msg.message_id
        )

    finally:
        safe_remove(file_path)


print("🚀 Pixo video bot ishga tushdi")
bot.infinity_polling(skip_pending=True)
