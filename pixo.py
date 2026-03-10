import telebot
import instaloader
import os

# =========================
# BOT TOKEN
# =========================
BOT_TOKEN = "8624963114:AAF1wIyfnfoY7Qu-Ct6jl6hXJQzD6Au9vB0"
bot = telebot.TeleBot(BOT_TOKEN)

# =========================
# DOWNLOAD PAPKA
# =========================
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# =========================
# INSTALOADER
# =========================
L = instaloader.Instaloader(
    dirname_pattern=DOWNLOAD_FOLDER,
    save_metadata=False,
    download_comments=False
)

# =========================
# START
# =========================
@bot.message_handler(commands=['start'])
def send_welcome(message):

    text = (
        "✨ *Assalomu alaykum!* ✨\n\n"
        "🤖 *Men Pixo Botman*\n"
        "📥 Instagram videolarini tez va oson yuklab beraman.\n\n"
        "📌 *Qanday ishlaydi?*\n"
        "1️⃣ Instagram Reel yoki Post linkini yuboring\n"
        "2️⃣ Men videoni yuklab olaman\n"
        "3️⃣ Sizga tayyor video yuboraman 🎬\n\n"
        "🚀 Shunchaki Instagram link yuboring va sinab ko‘ring!"
    )

    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# =========================
# VIDEO YUKLASH
# =========================
@bot.message_handler(func=lambda m: True)
def download_instagram_video(message):

    url = message.text.strip()

    if "instagram.com" not in url:
        bot.reply_to(message, "❌ Bu Instagram linki emas.\n\nIltimos to‘g‘ri link yuboring.")
        return

    msg = bot.reply_to(message, "⏳ Video yuklanmoqda...")

    try:
        shortcode = url.split("/")[-2]

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        if not post.is_video:
            bot.edit_message_text(
                "❌ Bu postda video yo‘q.",
                message.chat.id,
                msg.message_id
            )
            return

        # video yuklash
        L.download_post(post, target=DOWNLOAD_FOLDER)

        # mp4 faylni topish
        for file in os.listdir(DOWNLOAD_FOLDER):

            if file.endswith(".mp4"):

                path = os.path.join(DOWNLOAD_FOLDER, file)

                with open(path, "rb") as video:
                    bot.send_video(
                        message.chat.id,
                        video,
                        caption="🎬 Video yuklandi\n🤖 Pixo Bot"
                    )

                os.remove(path)

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:

        bot.edit_message_text(
            f"❌ Xatolik yuz berdi:\n{e}",
            message.chat.id,
            msg.message_id
        )

# =========================
# BOT ISHGA TUSHISHI
# =========================
print("Pixo bot ishga tushdi...")

bot.polling(none_stop=True)
