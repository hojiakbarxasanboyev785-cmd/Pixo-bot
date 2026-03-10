import telebot
import requests
import os
from flask import Flask
import threading

TOKEN = os.environ.get("8624963114:AAF1wIyfnfoY7Qu-Ct6jl6hXJQzD6Au9vB0")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
users = set()

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(url, file_path):
    response = requests.post(
        "https://api.cobalt.tools/",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json={"url": url},
        timeout=30
    )
    data = response.json()
    status = data.get("status")

    if status in ("stream", "redirect", "tunnel"):
        video_url = data["url"]
    elif status == "picker":
        video_url = data["picker"][0]["url"]
    else:
        raise Exception(f"Video topilmadi: {data}")

    r = requests.get(video_url, stream=True, timeout=60)
    with open(file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            f.write(chunk)

@bot.message_handler(commands=["start"])
def start(message):
    users.add(message.from_user.id)
    bot.send_message(message.chat.id,
        "✨ *Assalomu alaykum!*\n\n"
        "🤖 *Men Pixo Botman*\n"
        "📥 Instagram videolarini yuklab beraman.\n\n"
        f"👥 Foydalanuvchilar: *{len(users)}*\n\n"
        "⬇️ Instagram Reel yoki Post link yuboring!",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: True)
def handler(message):
    url = message.text.strip()
    users.add(message.from_user.id)

    if "instagram.com" not in url:
        bot.reply_to(message, "❌ Faqat Instagram link yuboring.")
        return

    msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")
    file_path = f"{DOWNLOAD_FOLDER}/{message.message_id}.mp4"

    try:
        download_video(url, file_path)

        with open(file_path, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                caption="🎬 Instagram Video\n🤖 Pixo Bot",
                supports_streaming=True
            )

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(
            f"❌ Xato: {e}",
            message.chat.id,
            msg.message_id
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def run_bot():
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot).start()

@app.route("/")
def index():
    return "🚀 Pixo Bot ishlayapti!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
