import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import random
import zipfile
import os
from datetime import datetime

# ===== API KALITLAR =====
BOT_TOKEN = "8624963114:AAEZXFcXUnEEd5-mbuZ4BXH1bC-HWuHX_FM"
WEATHER_API_KEY = "c4ba3f12c236fbe0bc8e5b383ba3df38"
NEWS_API_KEY = "bdec552c170b4892a669ebe6fad7eca2"

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}
user_data = {}
TEMP_DIR = os.path.expanduser("~")

# ===== VILOYAT VA TUMANLAR =====
HUDUDLAR = {
    "🏙 Toshkent shahri": [
        "Bektemir", "Chilonzor", "Hamza", "Mirzo Ulug'bek",
        "Mirobod", "Olmazar", "Sergeli", "Shayxontohur",
        "Uchtepa", "Yakkasaroy", "Yashnobod", "Yunusobod"
    ],
    "🌆 Toshkent viloyati": [
        "Angren", "Bekabad", "Bo'ka", "Bostonliq", "Chinoz",
        "Chirchiq", "Kibray", "Keles", "Nurafshon", "Ohangaron",
        "Olmaliq", "Oqqo'rg'on", "O'rtachirchiq", "Parkent",
        "Piskent", "Qibray", "Toshkent tumani", "Yangiyo'l",
        "Yuqorichirchiq", "Zangiota"
    ],
    "🏛 Samarqand viloyati": [
        "Bulung'ur", "Ishtixon", "Jomboy", "Kattaqo'rg'on",
        "Narpay", "Nurobod", "Oqdaryo", "Pastdarg'om",
        "Paxtachi", "Payariq", "Qo'shrabot", "Samarqand tumani",
        "Toyloq", "Urgut"
    ],
    "🕌 Buxoro viloyati": [
        "Buxoro tumani", "G'ijduvon", "Jondor", "Kogon",
        "Olot", "Peshku", "Qorako'l", "Qorovulbozor",
        "Romitan", "Shofirkon", "Vobkent"
    ],
    "🌿 Namangan viloyati": [
        "Chortoq", "Chust", "Davlatobod", "Kosonsoy",
        "Mingbuloq", "Namangan tumani", "Norin", "Pop",
        "To'raqo'rg'on", "Uchqo'rg'on", "Uychi", "Yangiqo'rg'on"
    ],
    "🌄 Farg'ona viloyati": [
        "Beshariq", "Bog'dod", "Buvayda", "Dang'ara",
        "Farg'ona tumani", "Furqat", "Marg'ilon", "Oltiariq",
        "Quva", "Qo'qon", "Rishton", "Toshloq",
        "Uchko'prik", "O'zbekiston tumani", "Yozyovon"
    ],
    "🏔 Andijon viloyati": [
        "Andijon tumani", "Asaka", "Baliqchi", "Bo'z",
        "Buloqboshi", "Izboskan", "Jalolquduq", "Marhamat",
        "Oltinkol", "Paxtaobod", "Qo'rg'ontepa", "Shahrixon",
        "Ulug'nor", "Xo'jaobod"
    ],
    "🌊 Xorazm viloyati": [
        "Bog'ot", "Gurlan", "Hazorasp", "Xiva tumani",
        "Xonqa", "Qo'shko'pir", "Shovot", "Tuproqqal'a",
        "Urganch tumani", "Yangiariq", "Yangibozor"
    ],
    "🏜 Qashqadaryo viloyati": [
        "Chiroqchi", "Dehqonobod", "G'uzor", "Kamashi",
        "Qarshi tumani", "Kasbi", "Kitob", "Koson",
        "Mirishkor", "Muborak", "Nishon", "Qamashi",
        "Shahrisabz tumani", "Yakkabog'"
    ],
    "🌋 Surxondaryo viloyati": [
        "Angor", "Bandixon", "Boysun", "Denov",
        "Jarqo'rg'on", "Muzrabot", "Oltinsoy", "Qiziriq",
        "Qumqo'rg'on", "Sariosiyo", "Sherobod", "Sho'rchi",
        "Termiz tumani", "Uzun"
    ],
    "⛰ Navoiy viloyati": [
        "Karmana", "Konimex", "Navbahor", "Navoiy tumani",
        "Nurota", "Qiziltepa", "Tomdi", "Uchquduq",
        "Xatirchi", "Zarafshon"
    ],
    "🌾 Jizzax viloyati": [
        "Arnasoy", "Baxmal", "Do'stlik", "Forish",
        "G'allaorol", "Jizzax tumani", "Mirzacho'l",
        "Paxtakor", "Sharof Rashidov", "Yangiobod",
        "Zarbdor", "Zomin"
    ],
    "🌻 Sirdaryo viloyati": [
        "Baxt", "Boyovut", "Guliston tumani", "Mirzaobod",
        "Oqoltin", "Sardoba", "Sayxunobod", "Sirdaryo tumani", "Xovos"
    ],
    "🏝 Qoraqalpog'iston": [
        "Amudaryo", "Beruniy", "Bozatov", "Chimboy",
        "Ellikkala", "Kegeyli", "Mo'ynoq", "Nukus tumani",
        "Qonliko'l", "Qorao'zak", "Shumanay", "Taxiatosh",
        "Taxtako'pir", "To'rtko'l", "Xo'jayli"
    ],
}

# ===== OB-HAVO TARJIMALAR =====
OB_HAVO_UZ = {
    "clear sky": "☀️ Ochiq osmon",
    "few clouds": "🌤 Oz bulutli",
    "scattered clouds": "⛅ Bulutli",
    "broken clouds": "☁️ Ko'p bulutli",
    "overcast clouds": "🌥 Quyuq bulut",
    "light rain": "🌦 Yengil yomg'ir",
    "moderate rain": "🌧 O'rtacha yomg'ir",
    "heavy intensity rain": "🌧 Kuchli yomg'ir",
    "very heavy rain": "⛈ Juda kuchli yomg'ir",
    "thunderstorm": "⛈ Momaqaldiroq",
    "thunderstorm with light rain": "⛈ Momaqaldiroqli yomg'ir",
    "thunderstorm with rain": "⛈ Momaqaldiroqli yomg'ir",
    "snow": "❄️ Qor",
    "light snow": "🌨 Yengil qor",
    "heavy snow": "❄️ Kuchli qor",
    "mist": "🌫 Tuman",
    "fog": "🌫 Qalin tuman",
    "haze": "🌫 Changlik",
    "drizzle": "🌦 Shivit yomg'ir",
    "light intensity drizzle": "🌦 Yengil shivit",
    "dust": "🌪 Chang bo'roni",
    "sand": "🌪 Qum bo'roni",
    "smoke": "🌫 Tutun",
    "squalls": "💨 Bo'ron",
    "tornado": "🌪 Tornado",
}

# ===== KITOBLAR =====
KITOB_MENU = [
    "📖 Badiiy",
    "🔬 Ilmiy",
    "📗 Darslik",
    "💼 Biznes",
    "🧘 Psixologiya",
    "💻 IT va Dasturlash",
]

KITOBLAR = {
    "📖 Badiiy": [
        ("O'tgan kunlar", "Abdulla Qodiriy", "O'zbek adabiyotining durdonasi"),
        ("Mehrobdan chayon", "Abdulla Qodiriy", "Tarixiy roman"),
        ("Sarob", "Abdulla Qahhor", "Zamonaviy o'zbek romani"),
        ("Yulduzli tunlar", "Pirimqul Qodirov", "Tarixiy roman"),
        ("O'tkinchi kunlar", "Oybek", "Klassik asar"),
        ("Qutlug' qon", "Oybek", "Tarixiy roman"),
    ],
    "🔬 Ilmiy": [
        ("Fizika asoslari", "Irodov", "Fizika masalalari to'plami"),
        ("Kimyo formulalar", "Turli mualliflar", "Kimyo qo'llanma"),
        ("Biologiya ensiklopediyasi", "Turli mualliflar", "To'liq biologiya"),
        ("Astronomiya asoslari", "Turli mualliflar", "Koinot haqida"),
        ("Matematika tahlili", "Fikhtengolts", "Oliy matematika"),
        ("Organik kimyo", "Morrison Boyd", "Kimyo darsligi"),
    ],
    "📗 Darslik": [
        ("Matematika 10-sinf", "O'zbek mualliflari", "Maktab darsligi"),
        ("Ingliz tili grammatikasi", "Raymond Murphy", "English Grammar in Use"),
        ("Tarix 11-sinf", "O'zbek mualliflari", "O'zbekiston tarixi"),
        ("Ona tili va adabiyot", "O'zbek mualliflari", "O'zbek tili"),
        ("Fizika 9-sinf", "O'zbek mualliflari", "Maktab fizikasi"),
        ("Kimyo 8-sinf", "O'zbek mualliflari", "Maktab kimyosi"),
    ],
    "💼 Biznes": [
        ("Rich Dad Poor Dad", "Robert Kiyosaki", "Moliyaviy savodxonlik"),
        ("7 ta odat", "Stephen Covey", "Muvaffaqiyat sirlari"),
        ("Biznes strategiyalari", "Michael Porter", "Raqobat ustunligi"),
        ("Marketing asoslari", "Philip Kotler", "Marketing klassikasi"),
        ("Zero to One", "Peter Thiel", "Startup qurish"),
        ("Thinking Fast and Slow", "Daniel Kahneman", "Qaror qabul qilish"),
    ],
    "🧘 Psixologiya": [
        ("Do'stlar orttirish", "Dale Carnegie", "Muloqot san'ati"),
        ("Fikrlash san'ati", "Rolf Dobelli", "Mantiqiy fikrlash"),
        ("Emotsional intellekt", "Daniel Goleman", "His-tuyg'ularni boshqarish"),
        ("Motivatsiya psixologiyasi", "Turli mualliflar", "Ichki kuch"),
        ("Atomic Habits", "James Clear", "Yaxshi odatlar shakllantirish"),
        ("Man's Search for Meaning", "Viktor Frankl", "Hayot ma'nosi"),
    ],
    "💻 IT va Dasturlash": [
        ("Python dasturlash", "Al Sweigart", "Automate the Boring Stuff"),
        ("Web dasturlash", "Jon Duckett", "HTML CSS JS"),
        ("SQL ma'lumotlar bazasi", "Alan Beaulieu", "SQL asoslari"),
        ("Algoritm va tuzilmalar", "Thomas Cormen", "CLRS klassikasi"),
        ("Clean Code", "Robert Martin", "Sifatli kod yozish"),
        ("The Pragmatic Programmer", "Hunt and Thomas", "Professional dasturlash"),
    ],
}

# ===== O'ZBEK YANGILIKLARI =====
UZBEK_NEWS = [
    {"sarlavha": "O'zbekiston iqtisodiyoti 2025 yilda 6.5 foizga o'sdi", "manba": "kun.uz", "url": "https://kun.uz", "vaqt": "Bugun"},
    {"sarlavha": "Toshkentda yangi metro liniyasi qurilishi boshlandi", "manba": "gazeta.uz", "url": "https://gazeta.uz", "vaqt": "Bugun"},
    {"sarlavha": "Prezident yangi ta'lim islohotlari farmonini imzoladi", "manba": "uza.uz", "url": "https://uza.uz", "vaqt": "Bugun"},
    {"sarlavha": "O'zbekistonda turizm sohasi rekord darajaga yetdi", "manba": "daryo.uz", "url": "https://daryo.uz", "vaqt": "Kecha"},
    {"sarlavha": "Samarqandda xalqaro investitsiya forumi muvaffaqiyatli o'tdi", "manba": "kun.uz", "url": "https://kun.uz", "vaqt": "2 kun oldin"},
    {"sarlavha": "Yoshlar uchun yangi startup grantlari e'lon qilindi", "manba": "gazeta.uz", "url": "https://gazeta.uz", "vaqt": "Bugun"},
    {"sarlavha": "O'zbekistonda yangi IT parklari va texnoparklar ochildi", "manba": "it.uz", "url": "https://it.uz", "vaqt": "Kecha"},
    {"sarlavha": "Milliy futbol terma jamoamiz muhim g'alaba qozondi", "manba": "sports.uz", "url": "https://sports.uz", "vaqt": "Bugun"},
    {"sarlavha": "O'zbekiston eksporti yangi tarixiy rekordga erishdi", "manba": "uza.uz", "url": "https://uza.uz", "vaqt": "3 kun oldin"},
    {"sarlavha": "Toshkentda xalqaro madaniyat va san'at festivali ochildi", "manba": "daryo.uz", "url": "https://daryo.uz", "vaqt": "Bugun"},
    {"sarlavha": "O'zbekistonda yangi zamonaviy shifoxonalar qurilmoqda", "manba": "uza.uz", "url": "https://uza.uz", "vaqt": "Kecha"},
    {"sarlavha": "Respublikamizda qishloq xo'jaligini modernizatsiya qilish davom etmoqda", "manba": "kun.uz", "url": "https://kun.uz", "vaqt": "2 kun oldin"},
]

# ===== DUNYO YANGILIKLARI (O'ZBEKCHA) =====
WORLD_NEWS = [
    {"sarlavha": "Sun'iy intellekt texnologiyalari jahon iqtisodiyotini o'zgartirmoqda", "manba": "BBC O'zbek", "url": "https://bbc.com/uzbek", "vaqt": "Bugun", "kategoria": "💻 Texnologiya"},
    {"sarlavha": "Jahon banki rivojlanayotgan mamlakatlarga yangi kredit ajratdi", "manba": "VOA O'zbek", "url": "https://voanews.com/uzbek", "vaqt": "Bugun", "kategoria": "💼 Iqtisodiyot"},
    {"sarlavha": "Evropa Ittifoqi yangi energetika dasturini e'lon qildi", "manba": "BBC O'zbek", "url": "https://bbc.com/uzbek", "vaqt": "Kecha", "kategoria": "⚡ Energetika"},
    {"sarlavha": "NASA yangi kosmik missiyani muvaffaqiyatli yakunladi", "manba": "Kun.uz xalqaro", "url": "https://kun.uz", "vaqt": "Bugun", "kategoria": "🚀 Fan"},
    {"sarlavha": "Xitoy iqtisodiyoti o'sishda davom etmoqda", "manba": "VOA O'zbek", "url": "https://voanews.com/uzbek", "vaqt": "2 kun oldin", "kategoria": "💼 Iqtisodiyot"},
    {"sarlavha": "Yaqin Sharqda tinchlik muzokaralari qayta boshlandi", "manba": "BBC O'zbek", "url": "https://bbc.com/uzbek", "vaqt": "Bugun", "kategoria": "🌍 Siyosat"},
    {"sarlavha": "Jahon sog'liqni saqlash tashkiloti yangi tavsiyalar berdi", "manba": "JSST", "url": "https://who.int", "vaqt": "Kecha", "kategoria": "🏥 Salomatlik"},
    {"sarlavha": "Iqlim o'zgarishi bo'yicha xalqaro konferensiya bo'lib o'tdi", "manba": "BBC O'zbek", "url": "https://bbc.com/uzbek", "vaqt": "3 kun oldin", "kategoria": "🌱 Ekologiya"},
    {"sarlavha": "Jahon chempionatida kutilmagan natijalar qayd etildi", "manba": "Sports.uz", "url": "https://sports.uz", "vaqt": "Bugun", "kategoria": "⚽ Sport"},
    {"sarlavha": "Elektr avtomobillar bozori rekord savdoga erishdi", "manba": "VOA O'zbek", "url": "https://voanews.com/uzbek", "vaqt": "Kecha", "kategoria": "🚗 Transport"},
    {"sarlavha": "OpenAI yangi sun'iy intellekt modeli taqdim etdi", "manba": "IT.uz", "url": "https://it.uz", "vaqt": "Bugun", "kategoria": "💻 Texnologiya"},
    {"sarlavha": "G20 sammitida global iqtisodiyot masalalari muhokama qilindi", "manba": "BBC O'zbek", "url": "https://bbc.com/uzbek", "vaqt": "2 kun oldin", "kategoria": "🌍 Siyosat"},
]

# ===== O'QUV MASHQLARI =====
MATH_TASKS = [
    ("2³ + √64 = ?", "8 + 8 = 16"),
    ("sin(90°) = ?", "1"),
    ("log₂(128) = ?", "7"),
    ("(a+b)² = ?", "a² + 2ab + b²"),
    ("5! = ?", "120"),
    ("∫x²dx = ?", "x³/3 + C"),
    ("π ≈ ?", "3.14159265"),
    ("12² - 5² = ?", "119"),
    ("√(16×25) = ?", "20"),
    ("lim(x→0) sinx/x = ?", "1"),
    ("cos(0°) = ?", "1"),
    ("tan(45°) = ?", "1"),
    ("2¹⁰ = ?", "1024"),
    ("e ≈ ?", "2.71828"),
    ("∑(1 to 100) = ?", "5050"),
]

SCIENCE_FACTS = [
    "⚡ Chaqmoq 300,000 km/s tezlikda harakat qiladi",
    "🧬 Inson DNKsi Quyoshgacha va qaytib yetadi",
    "🌍 Yer 4.5 milliard yil avval paydo bo'lgan",
    "🫀 Yurak bir kunda 100,000 marta uradi",
    "🧠 Inson miyasi 100 milliard neyrondan iborat",
    "🌊 Okean yer yuzasining 71 foizini qoplaydi",
    "☀️ Quyosh yorug'ligi Yerga 8 daqiqa 20 soniyada yetadi",
    "🦴 Tug'ilganda 270 ta suyak, kattada 206 ta",
    "💧 Suv H₂O — 2 vodorod + 1 kislorod",
    "🔬 Viruslar bakteriyalardan 10-100 marta kichik",
    "🌙 Oy Yerdan 384,400 km uzoqlikda joylashgan",
    "🐘 Fil 22 oy davomida homilador bo'ladi",
    "🌡 Absolyut nol harorat: -273.15°C",
    "💡 Yorug'lik 1 soniyada 7.5 marta Yer atrofini aylanadi",
    "🧪 Olmos — tabiatdagi eng qattiq modda",
]

LOGIC = [
    ("Qo'li bor lekin ishlamaydigan narsa nima?", "⌚ Soat!"),
    ("100 dan 1 gacha sanasang nechta 9 bor?", "20 ta!"),
    ("Inglizda eng ko'p ishlatiladigan harf?", "E harfi"),
    ("12 tuxumdan 6 marta olinsa nechta qoladi?", "0 ta — 6x2=12"),
    ("Suv tepaga chiqadigan joy qayer?", "Quvur ichida!"),
    ("Yong'inni o'chirmay qo'yish uchun nima qilish kerak?", "Yoqmaslik kerak!"),
    ("Eng uzun ingliz so'zi qaysi?", "smiles — s va s orasida 1 mile bor!"),
]

# ===== SAYOHAT =====
SAYOHAT = {
    "🏙 Toshkent": {
        "joylar": ["Xastimom masjidi", "Chorsu bozori", "Amir Temur xiyoboni", "Teleminora", "Eski shahar", "Muyi Muborak"],
        "taom": ["Non kabob", "Lagmon", "Dimlama", "Moshxo'rda", "Somsa"],
        "maslahat": "Metro bilan harakat qilish qulay va arzon! 🚇",
        "eng_yaxshi_vaqt": "Bahor va Kuz",
    },
    "🏛 Samarqand": {
        "joylar": ["Registon maydoni", "Shahi Zinda", "Guri Amir", "Bibi Xonim masjidi", "Ulug'bek rasadxonasi"],
        "taom": ["Samarqand noni", "Shashlik", "Somsa", "Mastava", "Naryn"],
        "maslahat": "Registon kechki yoritish shou — unutilmas taassurot! 🌟",
        "eng_yaxshi_vaqt": "Aprel-May, Sentabr-Oktyabr",
    },
    "🕌 Buxoro": {
        "joylar": ["Ark qal'asi", "Kalon minorasi", "Lyabi Hovuz", "Chor Minor", "Ismoil Somoniy maqbarasi"],
        "taom": ["Buxoro oshi", "Halim", "Chuchvara", "Qozonli go'sht"],
        "maslahat": "Kechqurun Lyabi Hovuz atrofida sayr — juda chiroyli! 🌙",
        "eng_yaxshi_vaqt": "Mart-May, Sentyabr-Noyabr",
    },
    "🏰 Xiva": {
        "joylar": ["Ichon Qal'a", "Juma masjidi", "Islam Xo'ja minorasi", "Kunya Ark", "Pahlavon Mahmud maqbarasi"],
        "taom": ["Xorazm oshi", "Shivit oshi", "Gurvak", "Mastava"],
        "maslahat": "UNESCO jahon merosi! Suratga olish uchun ideal. 📸",
        "eng_yaxshi_vaqt": "Aprel-Iyun, Avgust-Oktyabr",
    },
    "🌿 Namangan": {
        "joylar": ["Ota Valixon To'ra masjidi", "Kosonsoy sharsharasi", "Hoji Yusupboy Eshon", "Namangan bozori"],
        "taom": ["Namangan somsa", "Naryn", "Qozon kabob", "Chuchvara"],
        "maslahat": "O'zbekistonning 'bog' shahri — mevalar juda mazali! 🍑",
        "eng_yaxshi_vaqt": "Iyul-Avgust (meva mavsumi)",
    },
    "🌄 Farg'ona": {
        "joylar": ["Marg'ilon ipak fabrikasi", "Rishton kulolchilik", "Vodiy manzaralari", "Qo'qon xonligi saroyi"],
        "taom": ["Farg'ona palov", "Qozon kabob", "Chuchvara", "Lag'mon"],
        "maslahat": "Atlas ipak do'konlarini albatta ziyorat qiling! 🧵",
        "eng_yaxshi_vaqt": "Bahor va Yoz",
    },
}

# ===== SOS =====
SOS_DATA = {
    "sos_med": (
        "🏥 *TEZ YORDAM*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "📞 *103* — Tez tibbiy yordam\n"
        "📞 *1003* — Xususiy tez yordam\n\n"
        "⚠️ *Nima qilish kerak:*\n"
        "• Nafas olmasa — sun'iy nafas bering\n"
        "• Qon ketsa — bosib to'xtating\n"
        "• Harakatsiz qolsa — siljitmang\n"
        "• Aniq manzilni ayting!\n"
        "━━━━━━━━━━━━━━━━━━━━"
    ),
    "sos_fire": (
        "🚒 *YONG'IN XIZMATI*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "📞 *101* — Yong'in o'chirish\n\n"
        "⚠️ *Yong'inda nima qilish:*\n"
        "• Darhol binoni tark eting\n"
        "• Lift ishlatmang — zinapoyadan!\n"
        "• Tutun bo'lsa — egilib yuring\n"
        "• Eshikni yopib chiqing\n"
        "━━━━━━━━━━━━━━━━━━━━"
    ),
    "sos_police": (
        "👮 *POLITSIYA*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "📞 *102* — Politsiya\n"
        "📞 *1102* — Yo'l politsiyasi\n\n"
        "⚠️ *Maslahatlar:*\n"
        "• Tinch turing, vahima qilmang\n"
        "• Aniq manzil va holat ayting\n"
        "• Hujjatlashtiring (foto/video)\n"
        "━━━━━━━━━━━━━━━━━━━━"
    ),
    "sos_emergency": (
        "🌊 *FAVQULODDA VAZIYATLAR*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "📞 *1050* — FVV xizmati\n"
        "📞 *112* — Yagona xizmat\n\n"
        "⚠️ *Zilzila bo'lsa:*\n"
        "• Stol ostiga yashiring\n"
        "• Devordan uzoqda turing\n"
        "• Liftdan foydalanmang\n\n"
        "⚠️ *Sel bo'lsa:*\n"
        "• Yuqori joyga ko'tariling\n"
        "• Suvli yo'ldan o'tmang\n"
        "━━━━━━━━━━━━━━━━━━━━"
    ),
    "sos_all": (
        "☎️ *BARCHA MUHIM RAQAMLAR*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        "🏥 Tez yordam:       *103*\n"
        "🚒 Yong'in:           *101*\n"
        "👮 Politsiya:         *102*\n"
        "🌊 FVV:               *1050*\n"
        "📞 Yagona:            *112*\n"
        "🚗 Yo'l politsiyasi:  *1102*\n"
        "ℹ️ Ma'lumotnoma:     *109*\n"
        "🏦 Bank xizmati:      *1007*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔋 _Telefon o'chib borayotganda —_\n"
        "_faqat *112* ga qo'ng'iroq qiling!_"
    ),
}

# ==================== MENYULAR ====================

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(KeyboardButton("🌦 Ob-havo"),      KeyboardButton("💱 Valyuta kursi"))
    markup.row(KeyboardButton("📰 Yangiliklar"),   KeyboardButton("📊 Kripto narxlari"))
    markup.row(KeyboardButton("📚 Kitoblar"),      KeyboardButton("🧩 O'quv mashqlari"))
    markup.row(KeyboardButton("🧭 Sayohat"),       KeyboardButton("🚨 SOS"))
    return markup

# ==================== START ====================

@bot.message_handler(commands=['start'])
def start(message):
    user_states[message.chat.id] = None
    name = message.from_user.first_name or "Do'stim"
    text = (
        f"╔═══════════════════════╗\n"
        f"   👋 Salom, *{name}*!\n"
        f"╚═══════════════════════╝\n\n"
        f"🤖 Men *Pixo Bot*man!\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📋 *Mening xizmatlarim:*\n\n"
        f"🌦 *Ob-havo* — Viloyat va tuman\n"
        f"💱 *Valyuta* — CBU rasmiy kurs\n"
        f"📰 *Yangiliklar* — O'zbek va Dunyo\n"
        f"📊 *Kripto* — BTC, ETH, TON...\n"
        f"📚 *Kitoblar* — ZIP fayl + havolalar\n"
        f"🧩 *O'quv* — Matematika, IT, Mantiq\n"
        f"🧭 *Sayohat* — Shaharlar tavsiyasi\n"
        f"🚨 *SOS* — Favqulodda raqamlar\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👇 *Quyidan tanlang:*"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ==================== OB-HAVO ====================

@bot.message_handler(func=lambda m: m.text == "🌦 Ob-havo")
def weather_region(message):
    user_states[message.chat.id] = "weather_region"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for viloyat in HUDUDLAR.keys():
        markup.add(KeyboardButton(viloyat))
    markup.add(KeyboardButton("🔙 Orqaga"))
    bot.send_message(message.chat.id,
        "🗺 *Viloyatni tanlang:*",
        parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "weather_region")
def weather_district(message):
    if "Orqaga" in message.text:
        user_states[message.chat.id] = None
        bot.send_message(message.chat.id, "🏠 Asosiy menyu:", reply_markup=main_menu())
        return

    viloyat = None
    for k in HUDUDLAR:
        if k.strip() == message.text.strip() or k.split(" ", 1)[-1] in message.text:
            viloyat = k
            break

    if not viloyat:
        bot.send_message(message.chat.id, "❌ Viloyat topilmadi. Qayta tanlang.")
        return

    user_data[message.chat.id] = {"viloyat": viloyat}
    user_states[message.chat.id] = "weather_district"

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for tuman in HUDUDLAR[viloyat]:
        markup.add(KeyboardButton(tuman))
    markup.add(KeyboardButton("🔙 Viloyatga qaytish"))

    bot.send_message(message.chat.id,
        f"📍 *{viloyat}*\n🏘 Tumanni tanlang:",
        parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "weather_district")
def weather_show(message):
    if "Viloyatga qaytish" in message.text:
        user_states[message.chat.id] = "weather_region"
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for viloyat in HUDUDLAR.keys():
            markup.add(KeyboardButton(viloyat))
        markup.add(KeyboardButton("🔙 Orqaga"))
        bot.send_message(message.chat.id, "🗺 *Viloyatni tanlang:*",
            parse_mode="Markdown", reply_markup=markup)
        return

    tuman = message.text.strip()
    viloyat = user_data.get(message.chat.id, {}).get("viloyat", "")
    user_states[message.chat.id] = None

    bot.send_message(message.chat.id,
        f"⏳ *{tuman}* ob-havosi yuklanmoqda...", parse_mode="Markdown")

    try:
        url = (f"https://api.openweathermap.org/data/2.5/weather"
               f"?q={tuman},UZ&appid={WEATHER_API_KEY}&units=metric&lang=en")
        r = requests.get(url, timeout=10)
        d = r.json()

        if d.get("cod") == 200:
            temp     = d["main"]["temp"]
            feels    = d["main"]["feels_like"]
            humidity = d["main"]["humidity"]
            wind     = d["wind"]["speed"]
            pressure = d["main"]["pressure"]
            desc_en  = d["weather"][0]["description"].lower()
            desc_uz  = OB_HAVO_UZ.get(desc_en, desc_en.capitalize())
            w_id     = d["weather"][0]["id"]

            if w_id == 800:        icon = "☀️"
            elif 801 <= w_id <= 804: icon = "⛅"
            elif w_id < 300:       icon = "⛈"
            elif w_id < 400:       icon = "🌦"
            elif w_id < 600:       icon = "🌧"
            elif w_id < 700:       icon = "❄️"
            else:                  icon = "🌫"

            if temp >= 35:   t_baho = "🥵 Juda issiq"
            elif temp >= 25: t_baho = "☀️ Issiq"
            elif temp >= 15: t_baho = "😊 Iliq"
            elif temp >= 5:  t_baho = "🧥 Salqin"
            elif temp >= 0:  t_baho = "🥶 Sovuq"
            else:            t_baho = "❄️ Qattiq sovuq"

            text = (
                f"{icon} *{tuman} Ob-Havosi*\n"
                f"📍 _{viloyat}_\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🌡 Harorat:        *{temp}°C*\n"
                f"🤔 His qilinadi:  *{feels}°C*\n"
                f"💧 Namlik:         *{humidity}%*\n"
                f"💨 Shamol:         *{wind} m/s*\n"
                f"📊 Bosim:          *{pressure} hPa*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 Holat:  *{desc_uz}*\n"
                f"🌡 Baho:   *{t_baho}*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🕐 {datetime.now().strftime('%H:%M  |  %d.%m.%Y')}"
            )
        else:
            viloyat_nomi = viloyat.split(" ", 1)[-1].replace(" viloyati", "").replace(" shahri", "")
            url2 = (f"https://api.openweathermap.org/data/2.5/weather"
                    f"?q={viloyat_nomi},UZ&appid={WEATHER_API_KEY}&units=metric&lang=en")
            r2 = requests.get(url2, timeout=10)
            d2 = r2.json()
            if d2.get("cod") == 200:
                temp = d2["main"]["temp"]
                desc_en = d2["weather"][0]["description"].lower()
                desc_uz = OB_HAVO_UZ.get(desc_en, desc_en.capitalize())
                text = (
                    f"🌡 *{tuman}* _(taxminiy — {viloyat_nomi})_\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🌡 Harorat: *{temp}°C*\n"
                    f"📋 Holat: *{desc_uz}*\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🕐 {datetime.now().strftime('%H:%M  |  %d.%m.%Y')}"
                )
            else:
                text = f"❌ *{tuman}* uchun ob-havo topilmadi."

    except Exception as e:
        text = f"⚠️ Xatolik: `{e}`"

    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ==================== VALYUTA ====================

@bot.message_handler(func=lambda m: m.text == "💱 Valyuta kursi")
def currency(message):
    bot.send_message(message.chat.id, "⏳ Valyuta kurslari yuklanmoqda...")
    try:
        url = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.encoding = "utf-8"
        data = r.json()

        SHOW = {
            "USD": "🇺🇸", "EUR": "🇪🇺", "RUB": "🇷🇺",
            "GBP": "🇬🇧", "JPY": "🇯🇵", "CNY": "🇨🇳",
            "KZT": "🇰🇿", "KRW": "🇰🇷", "TRY": "🇹🇷",
            "AED": "🇦🇪", "SAR": "🇸🇦", "GEL": "🇬🇪",
        }

        text = (
            f"💱 *Markaziy Bank Valyuta Kurslari*\n"
            f"📅 {datetime.now().strftime('%d.%m.%Y')}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        for item in data:
            ccy = item.get("Ccy", "")
            if ccy in SHOW:
                rate = float(item["Rate"])
                diff = float(item.get("Diff", 0))
                arrow = "📈" if diff > 0 else ("📉" if diff < 0 else "➡️")
                text += f"{SHOW[ccy]} *{ccy}*:  `{rate:>12,.2f}` so'm  {arrow}\n"
        text += "\n━━━━━━━━━━━━━━━━━━━━\n🏦 _Manba: cbu.uz_"
        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Xatolik: `{e}`",
                         parse_mode="Markdown", reply_markup=main_menu())

# ==================== YANGILIKLAR ====================

@bot.message_handler(func=lambda m: m.text == "📰 Yangiliklar")
def news_menu(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🇺🇿 O'zbek yangiliklari", callback_data="news_uz"),
        InlineKeyboardButton("🌍 Dunyo yangiliklari",   callback_data="news_world")
    )
    bot.send_message(message.chat.id, "📰 *Qaysi yangiliklar?*",
                     parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("news_"))
def news_fetch(call):
    bot.answer_callback_query(call.id, "⏳ Yuklanmoqda...")
    cid = call.message.chat.id

    if call.data == "news_uz":
        news_list = random.sample(UZBEK_NEWS, min(6, len(UZBEK_NEWS)))
        text = (
            f"📰 *O'zbekiston Yangiliklari*\n"
            f"📅 {datetime.now().strftime('%d.%m.%Y  %H:%M')}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        for i, n in enumerate(news_list, 1):
            text += (
                f"*{i}.* {n['sarlavha']}\n"
                f"   🗞 _{n['manba']}_  •  🕐 _{n['vaqt']}_\n"
                f"   🔗 [Batafsil o'qish]({n['url']})\n\n"
            )
        text += (
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 *To'liq yangiliklar:*\n"
            f"[kun.uz](https://kun.uz) • [gazeta.uz](https://gazeta.uz)\n"
            f"[daryo.uz](https://daryo.uz) • [uza.uz](https://uza.uz)"
        )
        bot.send_message(cid, text, parse_mode="Markdown",
                         disable_web_page_preview=True, reply_markup=main_menu())

    else:
        news_list = random.sample(WORLD_NEWS, min(6, len(WORLD_NEWS)))
        text = (
            f"🌍 *Dunyo Yangiliklari*\n"
            f"📅 {datetime.now().strftime('%d.%m.%Y  %H:%M')}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        for i, n in enumerate(news_list, 1):
            text += (
                f"*{i}.* {n['kategoria']}\n"
                f"   {n['sarlavha']}\n"
                f"   🗞 _{n['manba']}_  •  🕐 _{n['vaqt']}_\n"
                f"   🔗 [Batafsil o'qish]({n['url']})\n\n"
            )
        text += (
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 *To'liq xalqaro yangiliklar:*\n"
            f"[BBC O'zbek](https://bbc.com/uzbek) • [VOA O'zbek](https://voanews.com/uzbek)"
        )
        bot.send_message(cid, text, parse_mode="Markdown",
                         disable_web_page_preview=True, reply_markup=main_menu())

# ==================== KRIPTO ====================

@bot.message_handler(func=lambda m: m.text == "📊 Kripto narxlari")
def crypto(message):
    bot.send_message(message.chat.id, "⏳ Kripto narxlar yuklanmoqda...")
    try:
        ids = "bitcoin,ethereum,binancecoin,solana,toncoin,ripple,cardano,dogecoin,polkadot,avalanche-2"
        url = (f"https://api.coingecko.com/api/v3/simple/price"
               f"?ids={ids}&vs_currencies=usd&include_24hr_change=true")
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        data = r.json()

        COINS = [
            ("bitcoin",     "₿",  "Bitcoin",   "BTC"),
            ("ethereum",    "Ξ",  "Ethereum",  "ETH"),
            ("binancecoin", "🔶", "BNB",        "BNB"),
            ("solana",      "◎",  "Solana",    "SOL"),
            ("toncoin",     "💎", "TON",        "TON"),
            ("ripple",      "💧", "XRP",        "XRP"),
            ("cardano",     "🔵", "Cardano",   "ADA"),
            ("dogecoin",    "🐕", "Dogecoin",  "DOGE"),
            ("polkadot",    "⚪", "Polkadot",  "DOT"),
            ("avalanche-2", "🔺", "Avalanche", "AVAX"),
        ]

        text = (
            f"📊 *Kripto Valyuta Narxlari*\n"
            f"🕐 {datetime.now().strftime('%H:%M  |  %d.%m.%Y')}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        for cid_c, icon, name, sym in COINS:
            if cid_c in data:
                price  = data[cid_c].get("usd", 0)
                change = data[cid_c].get("usd_24h_change", 0)
                arrow  = "📈" if change >= 0 else "📉"
                p_str  = f"${price:,.2f}" if price >= 1 else f"${price:.5f}"
                text  += f"{icon} *{name}* `{sym}`\n   💵 {p_str}   {arrow} `{change:+.2f}%`\n\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n🔗 _Manba: CoinGecko_"
        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Xatolik: `{e}`",
                         parse_mode="Markdown", reply_markup=main_menu())

# ==================== KITOBLAR ====================

@bot.message_handler(func=lambda m: m.text == "📚 Kitoblar")
def books_menu(message):
    user_states[message.chat.id] = "books"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for k in KITOB_MENU:
        markup.add(KeyboardButton(k))
    markup.add(KeyboardButton("🔙 Orqaga"))
    bot.send_message(message.chat.id,
        "📚 *Kitob turini tanlang:*",
        parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "books")
def books_send(message):
    txt = message.text.strip()

    if "Orqaga" in txt:
        user_states[message.chat.id] = None
        bot.send_message(message.chat.id, "🏠 Asosiy menyu:", reply_markup=main_menu())
        return

    tur = None
    for k in KITOBLAR:
        if k == txt or k.split(" ", 1)[-1].strip() == txt.split(" ", 1)[-1].strip():
            tur = k
            break

    user_states[message.chat.id] = None

    if tur:
        bot.send_message(message.chat.id,
            f"⏳ *{tur}* kitoblari tayyorlanmoqda...", parse_mode="Markdown")

        zip_path = os.path.join(TEMP_DIR, "pixo_kitoblar.zip")

        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for i, (nom, muallif, tavsif) in enumerate(KITOBLAR[tur], 1):
                    content = (
                        f"╔══════════════════════════════════════╗\n"
                        f"         📚 PIXO BOT KUTUBXONASI\n"
                        f"╚══════════════════════════════════════╝\n\n"
                        f"📖 Kitob nomi : {nom}\n"
                        f"✍️  Muallif    : {muallif}\n"
                        f"📝 Tavsif     : {tavsif}\n"
                        f"📂 Kategoriya : {tur}\n\n"
                        f"{'='*42}\n"
                        f"          🔗 YUKLAB OLISH HAVOLALARI\n"
                        f"{'='*42}\n\n"
                        f"1. Google Books:\n"
                        f"   https://books.google.com/search?q={nom.replace(' ', '+')}\n\n"
                        f"2. Z-Library (bepul kutubxona):\n"
                        f"   https://z-lib.org\n\n"
                        f"3. Ziyouz.com (O'zbek kitoblari):\n"
                        f"   https://ziyouz.com\n\n"
                        f"4. Archive.org (bepul):\n"
                        f"   https://archive.org/search?query={nom.replace(' ', '+')}\n\n"
                        f"5. PDF Drive:\n"
                        f"   https://www.pdfdrive.com/search?q={nom.replace(' ', '+')}\n\n"
                        f"6. Litres.ru:\n"
                        f"   https://litres.ru/search/?q={nom.replace(' ', '+')}\n\n"
                        f"{'='*42}\n"
                        f"🤖 Pixo Bot | 📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                    )
                    safe = f"{i:02d}_{nom[:25].replace('/', '_').replace(':', '_')}.txt"
                    zf.writestr(safe, content)

                readme = (
                    f"📚 PIXO BOT — {tur.upper()} KITOBLARI\n"
                    f"{'='*42}\n\n"
                    f"Bu ZIP faylda {len(KITOBLAR[tur])} ta kitob havolasi mavjud.\n\n"
                    f"Har bir .txt faylni oching va\n"
                    f"havolalardan kitobni bepul yuklab oling!\n\n"
                    f"BEPUL SAYTLAR:\n"
                    f"• z-lib.org\n"
                    f"• ziyouz.com\n"
                    f"• archive.org\n"
                    f"• pdfdrive.com\n\n"
                    f"🤖 Pixo Bot | {datetime.now().strftime('%d.%m.%Y')}\n"
                )
                zf.writestr("00_README.txt", readme)

            list_text = (
                f"📚 *{tur}* kitoblari:\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
            )
            for i, (nom, muallif, _) in enumerate(KITOBLAR[tur], 1):
                list_text += f"  *{i}.* {nom}\n      _✍️ {muallif}_\n\n"
            list_text += "━━━━━━━━━━━━━━━━━━━━\n📦 ZIP yuborilmoqda..."

            bot.send_message(message.chat.id, list_text, parse_mode="Markdown")

            with open(zip_path, "rb") as f:
                bot.send_document(
                    message.chat.id, f,
                    caption=(
                        f"📚 *{tur}*\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"📁 {len(KITOBLAR[tur])} ta kitob + README\n"
                        f"💡 Har bir faylda 6 ta yuklab olish havolasi\n"
                        f"✅ Bepul saytlardan yuklab oling!"
                    ),
                    parse_mode="Markdown"
                )

            if os.path.exists(zip_path):
                os.remove(zip_path)

            bot.send_message(message.chat.id,
                "✅ *Muvaffaqiyatli yuborildi!*",
                parse_mode="Markdown", reply_markup=main_menu())

        except Exception as e:
            if os.path.exists(zip_path):
                try:
                    os.remove(zip_path)
                except:
                    pass

            fallback = (
                f"📚 *{tur}* kitoblari:\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
            )
            for i, (nom, muallif, _) in enumerate(KITOBLAR[tur], 1):
                fallback += (
                    f"*{i}. {nom}*\n"
                    f"✍️ _{muallif}_\n"
                    f"🔗 [Google Books](https://books.google.com/search?q={nom.replace(' ', '+')})\n\n"
                )
            fallback += (
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📌 *Bepul kutubxonalar:*\n"
                f"• [Z-Library](https://z-lib.org)\n"
                f"• [Ziyouz.com](https://ziyouz.com)\n"
                f"• [PDF Drive](https://pdfdrive.com)\n"
                f"• [Archive.org](https://archive.org)"
            )
            bot.send_message(message.chat.id, fallback,
                           parse_mode="Markdown",
                           disable_web_page_preview=False,
                           reply_markup=main_menu())
    else:
        user_states[message.chat.id] = "books"
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for k in KITOB_MENU:
            markup.add(KeyboardButton(k))
        markup.add(KeyboardButton("🔙 Orqaga"))
        bot.send_message(message.chat.id, "❌ Tugmani bosing:", reply_markup=markup)

# ==================== O'QUV MASHQLARI ====================

@bot.message_handler(func=lambda m: m.text == "🧩 O'quv mashqlari")
def edu_menu(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🧮 Matematika",    callback_data="edu_math"),
        InlineKeyboardButton("🔬 Ilmiy faktlar", callback_data="edu_science"),
        InlineKeyboardButton("🧠 Mantiq o'yini", callback_data="edu_logic"),
        InlineKeyboardButton("💻 IT kurslar",    callback_data="edu_it"),
        InlineKeyboardButton("🗣 Til o'rganish", callback_data="edu_lang"),
        InlineKeyboardButton("📅 Dars jadvali",  callback_data="edu_schedule"),
    )
    bot.send_message(message.chat.id,
        "🧩 *O'quv Mashqlari*\n━━━━━━━━━━━━━━━━━━━━\nNimani o'rganasiz?",
        parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("edu_"))
def edu_callback(call):
    bot.answer_callback_query(call.id)
    d = call.data

    if d == "edu_math":
        tasks = random.sample(MATH_TASKS, min(5, len(MATH_TASKS)))
        text = "🧮 *Matematika Mashqlari*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for i, (q, a) in enumerate(tasks, 1):
            text += f"*{i}.* _{q}_\n✅ `{a}`\n\n"

    elif d == "edu_science":
        facts = random.sample(SCIENCE_FACTS, min(5, len(SCIENCE_FACTS)))
        text = "🔬 *Qiziqarli Ilmiy Faktlar*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for i, f in enumerate(facts, 1):
            text += f"*{i}.* {f}\n\n"

    elif d == "edu_logic":
        q, a = random.choice(LOGIC)
        text = (
            f"🧠 *Mantiq O'yini*\n━━━━━━━━━━━━━━━━━━━━\n\n"
            f"❓ *Savol:*\n_{q}_\n\n"
            f"||✅ *Javob:* {a}||"
        )

    elif d == "edu_it":
        text = (
            "💻 *IT Kurslar va Resurslar*\n━━━━━━━━━━━━━━━━━━━━\n\n"
            "🐍 *Python:*\n   [python.org](https://python.org)\n\n"
            "🌐 *Web:*\n   [freecodecamp.org](https://freecodecamp.org)\n\n"
            "📱 *Flutter:*\n   [flutter.dev](https://flutter.dev)\n\n"
            "🤖 *ML/AI:*\n   [coursera.org](https://coursera.org)\n\n"
            "🛢 *SQL:*\n   [sqlzoo.net](https://sqlzoo.net)\n\n"
            "📺 *O'zbek kanallar:*\n   IT Park Uzbekistan"
        )

    elif d == "edu_lang":
        text = (
            "🗣 *Til O'rganish Resurslari*\n━━━━━━━━━━━━━━━━━━━━\n\n"
            "🇬🇧 *Ingliz:*\n   [duolingo.com](https://duolingo.com)\n\n"
            "🇷🇺 *Rus:*\n   [russiapod101.com](https://russiapod101.com)\n\n"
            "🇩🇪 *Nemis:*\n   [dw.com](https://dw.com/en/learn-german)\n\n"
            "🇰🇷 *Koreys:*\n   [talktomeinkorean.com](https://talktomeinkorean.com)\n\n"
            "🇨🇳 *Xitoy:*\n   [hellochinese.com](https://hellochinese.com)\n\n"
            "🇦🇪 *Arab:*\n   [arabicpod101.com](https://arabicpod101.com)"
        )

    elif d == "edu_schedule":
        text = (
            "📅 *Kunlik Dars Jadvali*\n━━━━━━━━━━━━━━━━━━━━\n\n"
            "🌅 `07:00` — Uyg'onish + mashq\n"
            "📖 `08:00` — Asosiy fanlar\n"
            "☕ `10:00` — Dam olish\n"
            "💻 `10:15` — Dasturlash\n"
            "🍽 `12:00` — Tushlik\n"
            "🗣 `13:00` — Til o'rganish\n"
            "📚 `15:00` — Uy vazifasi\n"
            "🏃 `17:00` — Sport\n"
            "🔬 `19:00` — Ilmiy fanlar\n"
            "🌙 `22:00` — Uyqu\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💡 _Har kuni 1% yaxshilansang — 1 yilda 37 marta o'sasan!_ 🚀"
        )
    else:
        text = "❌ Noma'lum"

    bot.send_message(call.message.chat.id, text,
                     parse_mode="Markdown", reply_markup=main_menu())

# ==================== SAYOHAT ====================

@bot.message_handler(func=lambda m: m.text == "🧭 Sayohat")
def travel_menu(message):
    user_states[message.chat.id] = "travel"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for city in SAYOHAT.keys():
        markup.add(KeyboardButton(city))
    markup.add(KeyboardButton("🔙 Orqaga"))
    bot.send_message(message.chat.id,
        "✈️ *Qaysi shaharga borasiz?*",
        parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "travel")
def travel_info(message):
    if "Orqaga" in message.text:
        user_states[message.chat.id] = None
        bot.send_message(message.chat.id, "🏠 Asosiy menyu:", reply_markup=main_menu())
        return

    city = message.text.strip()
    user_states[message.chat.id] = None

    found = None
    for k in SAYOHAT:
        if k == city or k.split(" ", 1)[-1] in city:
            found = k
            break

    if found:
        d = SAYOHAT[found]
        text = (
            f"✈️ *{found}*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🏛 *Ko'rish kerak bo'lgan joylar:*\n" +
            "\n".join(f"  • {j}" for j in d["joylar"]) +
            f"\n\n🍽 *Mahalliy taomlar:*\n" +
            "\n".join(f"  • {t}" for t in d["taom"]) +
            f"\n\n🗓 *Eng yaxshi vaqt:* _{d['eng_yaxshi_vaqt']}_\n\n"
            f"💡 *Maslahat:* _{d['maslahat']}_\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
    else:
        text = "❌ Bu shahar ro'yxatda yo'q."

    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ==================== SOS ====================

@bot.message_handler(func=lambda m: m.text == "🚨 SOS")
def sos(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🏥 Tez yordam",      callback_data="sos_med"),
        InlineKeyboardButton("🚒 Yong'in",         callback_data="sos_fire"),
        InlineKeyboardButton("👮 Politsiya",       callback_data="sos_police"),
        InlineKeyboardButton("🌊 Favqulodda",      callback_data="sos_emergency"),
        InlineKeyboardButton("☎️ Barcha raqamlar", callback_data="sos_all"),
    )
    bot.send_message(message.chat.id,
        "🚨 *FAVQULODDA YORDAM*\n━━━━━━━━━━━━━━━━━━━━\n❗ Qanday yordam kerak?",
        parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("sos_"))
def sos_callback(call):
    bot.answer_callback_query(call.id)
    text = SOS_DATA.get(call.data, "❌ Topilmadi")
    bot.send_message(call.message.chat.id, text,
                     parse_mode="Markdown", reply_markup=main_menu())

# ==================== NOMA'LUM ====================

@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(message.chat.id,
        "❓ *Tushunmadim.*\nQuyidagi menyudan tanlang 👇",
        parse_mode="Markdown", reply_markup=main_menu())

# ==================== ISHGA TUSHIRISH ====================

if __name__ == "__main__":
    print("╔════════════════════════════╗")
    print("   🤖 PIXO BOT ISHGA TUSHDI!")
    print("╚════════════════════════════╝")
    print(f"⏰ {datetime.now().strftime('%H:%M:%S  %d.%m.%Y')}")
    print("✅ Barcha funksiyalar faol")
    print("━" * 30)
    bot.infinity_polling(timeout=30, long_polling_timeout=30)
