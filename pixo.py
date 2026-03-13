import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import random
import zipfile
import os
from datetime import datetime
from flask import Flask, request

BOT_TOKEN = os.environ.get("8624963114:AAEZXFcXUnEEd5-mbuZ4BXH1bC-HWuHX_FM", "")
WEATHER_API_KEY = os.environ.get("c4ba3f12c236fbe0bc8e5b383ba3df38", "")
WEBHOOK_URL = os.environ.get("https://pixo-bot-1.onrender.com/set_webhook", "")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

user_states = {}
user_data = {}
TEMP_DIR = "/tmp"

HUDUDLAR = {
    "🏙 Toshkent shahri": ["🏢 Bektemir","🏢 Chilonzor","🏢 Hamza","🏢 Mirzo Ulug'bek","🏢 Mirobod","🏢 Olmazar","🏢 Sergeli","🏢 Shayxontohur","🏢 Uchtepa","🏢 Yakkasaroy","🏢 Yashnobod","🏢 Yunusobod"],
    "🌆 Toshkent viloyati": ["🏘 Angren","🏘 Bekabad","🏘 Bo'ka","🏘 Bostonliq","🏘 Chinoz","🏘 Chirchiq","🏘 Kibray","🏘 Keles","🏘 Nurafshon","🏘 Ohangaron","🏘 Olmaliq","🏘 Oqqo'rg'on","🏘 O'rtachirchiq","🏘 Parkent","🏘 Piskent","🏘 Qibray","🏘 Toshkent tumani","🏘 Yangiyo'l","🏘 Yuqorichirchiq","🏘 Zangiota"],
    "🏛 Samarqand viloyati": ["🏘 Bulung'ur","🏘 Ishtixon","🏘 Jomboy","🏘 Kattaqo'rg'on","🏘 Narpay","🏘 Nurobod","🏘 Oqdaryo","🏘 Pastdarg'om","🏘 Paxtachi","🏘 Payariq","🏘 Qo'shrabot","🏘 Samarqand tumani","🏘 Toyloq","🏘 Urgut"],
    "🕌 Buxoro viloyati": ["🏘 Buxoro tumani","🏘 G'ijduvon","🏘 Jondor","🏘 Kogon","🏘 Olot","🏘 Peshku","🏘 Qorako'l","🏘 Qorovulbozor","🏘 Romitan","🏘 Shofirkon","🏘 Vobkent"],
    "🌿 Namangan viloyati": ["🏘 Chortoq","🏘 Chust","🏘 Davlatobod","🏘 Kosonsoy","🏘 Mingbuloq","🏘 Namangan tumani","🏘 Norin","🏘 Pop","🏘 To'raqo'rg'on","🏘 Uchqo'rg'on","🏘 Uychi","🏘 Yangiqo'rg'on"],
    "🌄 Farg'ona viloyati": ["🏘 Beshariq","🏘 Bog'dod","🏘 Buvayda","🏘 Dang'ara","🏘 Farg'ona tumani","🏘 Furqat","🏘 Marg'ilon","🏘 Oltiariq","🏘 Quva","🏘 Qo'qon","🏘 Rishton","🏘 Toshloq","🏘 Uchko'prik","🏘 O'zbekiston tumani","🏘 Yozyovon"],
    "🏔 Andijon viloyati": ["🏘 Andijon tumani","🏘 Asaka","🏘 Baliqchi","🏘 Bo'z","🏘 Buloqboshi","🏘 Izboskan","🏘 Jalolquduq","🏘 Marhamat","🏘 Oltinkol","🏘 Paxtaobod","🏘 Qo'rg'ontepa","🏘 Shahrixon","🏘 Ulug'nor","🏘 Xo'jaobod"],
    "🌊 Xorazm viloyati": ["🏘 Bog'ot","🏘 Gurlan","🏘 Hazorasp","🏘 Xiva tumani","🏘 Xonqa","🏘 Qo'shko'pir","🏘 Shovot","🏘 Tuproqqal'a","🏘 Urganch tumani","🏘 Yangiariq","🏘 Yangibozor"],
    "🏜 Qashqadaryo viloyati": ["🏘 Chiroqchi","🏘 Dehqonobod","🏘 G'uzor","🏘 Kamashi","🏘 Qarshi tumani","🏘 Kasbi","🏘 Kitob","🏘 Koson","🏘 Mirishkor","🏘 Muborak","🏘 Nishon","🏘 Qamashi","🏘 Shahrisabz tumani","🏘 Yakkabog'"],
    "🌋 Surxondaryo viloyati": ["🏘 Angor","🏘 Bandixon","🏘 Boysun","🏘 Denov","🏘 Jarqo'rg'on","🏘 Muzrabot","🏘 Oltinsoy","🏘 Qiziriq","🏘 Qumqo'rg'on","🏘 Sariosiyo","🏘 Sherobod","🏘 Sho'rchi","🏘 Termiz tumani","🏘 Uzun"],
    "⛰ Navoiy viloyati": ["🏘 Karmana","🏘 Konimex","🏘 Navbahor","🏘 Navoiy tumani","🏘 Nurota","🏘 Qiziltepa","🏘 Tomdi","🏘 Uchquduq","🏘 Xatirchi","🏘 Zarafshon"],
    "🌾 Jizzax viloyati": ["🏘 Arnasoy","🏘 Baxmal","🏘 Do'stlik","🏘 Forish","🏘 G'allaorol","🏘 Jizzax tumani","🏘 Mirzacho'l","🏘 Paxtakor","🏘 Sharof Rashidov","🏘 Yangiobod","🏘 Zarbdor","🏘 Zomin"],
    "🌻 Sirdaryo viloyati": ["🏘 Baxt","🏘 Boyovut","🏘 Guliston tumani","🏘 Mirzaobod","🏘 Oqoltin","🏘 Sardoba","🏘 Sayxunobod","🏘 Sirdaryo tumani","🏘 Xovos"],
    "🏝 Qoraqalpog'iston": ["🏘 Amudaryo","🏘 Beruniy","🏘 Bozatov","🏘 Chimboy","🏘 Ellikkala","🏘 Kegeyli","🏘 Mo'ynoq","🏘 Nukus tumani","🏘 Qonliko'l","🏘 Qorao'zak","🏘 Shumanay","🏘 Taxiatosh","🏘 Taxtako'pir","🏘 To'rtko'l","🏘 Xo'jayli"],
}

OB_HAVO_UZ = {
    "clear sky":"☀️ Ochiq osmon","few clouds":"🌤 Oz bulutli","scattered clouds":"⛅ Bulutli",
    "broken clouds":"☁️ Ko'p bulutli","overcast clouds":"🌥 Quyuq bulut","light rain":"🌦 Yengil yomg'ir",
    "moderate rain":"🌧 O'rtacha yomg'ir","heavy intensity rain":"🌧 Kuchli yomg'ir",
    "very heavy rain":"⛈ Juda kuchli yomg'ir","thunderstorm":"⛈ Momaqaldiroq",
    "thunderstorm with light rain":"⛈ Momaqaldiroqli yomg'ir","thunderstorm with rain":"⛈ Momaqaldiroqli yomg'ir",
    "snow":"❄️ Qor","light snow":"🌨 Yengil qor","heavy snow":"❄️ Kuchli qor",
    "mist":"🌫 Tuman","fog":"🌫 Qalin tuman","haze":"🌫 Changlik","drizzle":"🌦 Shivit yomg'ir",
    "light intensity drizzle":"🌦 Yengil shivit","dust":"🌪 Chang bo'roni","sand":"🌪 Qum bo'roni",
    "smoke":"🌫 Tutun","squalls":"💨 Bo'ron","tornado":"🌪 Tornado",
}

KITOB_MENU = ["📖 Badiiy","🔬 Ilmiy","📗 Darslik","💼 Biznes","🧘 Psixologiya","💻 IT va Dasturlash"]

KITOBLAR = {
    "📖 Badiiy": [
        ("O'tgan kunlar","Abdulla Qodiriy","O'zbek adabiyotining birinchi romani.","https://ziyouz.com/books/uzbek_classic/abdulla_qodiriy/Abdulla%20Qodiriy%20-%20O%27tgan%20kunlar%20(ziyouz.com).pdf"),
        ("Mehrobdan chayon","Abdulla Qodiriy","Andijon xonligi davrida ayol taqdiri haqida tarixiy roman.","https://ziyouz.com/books/uzbek_classic/abdulla_qodiriy/Abdulla%20Qodiriy%20-%20Mehrobdan%20chayon%20(ziyouz.com).pdf"),
        ("Sarob","Abdulla Qahhor","Insoniy zaiflik va aldanish haqidagi psixologik roman.","https://ziyouz.com/books/uzbek_classic/abdulla_qahhor/Abdulla%20Qahhor%20-%20Sarob%20(ziyouz.com).pdf"),
        ("Yulduzli tunlar","Pirimqul Qodirov","Bobur Mirzo hayoti haqida mashhur tarixiy roman.","https://ziyouz.com/books/uzbek_classic/pirimqul_qodirov/Pirimqul%20Qodirov%20-%20Yulduzli%20tunlar%20(ziyouz.com).pdf"),
        ("Ulug'bek xazinasi","Odil Yoqubov","Mirzo Ulug'bek va ilm-fan haqida buyuk tarixiy roman.","https://ziyouz.com/books/uzbek_classic/odil_yoqubov/Odil%20Yoqubov%20-%20Ulugbek%20xazinasi%20(ziyouz.com).pdf"),
        ("Qutlug' qon","Oybek","XX asr boshida o'zbek xalqining ozodlik kurashi haqida roman.","https://ziyouz.com/books/uzbek_classic/oybek/Oybek%20-%20Qutlug%27%20qon%20(ziyouz.com).pdf"),
    ],
    "🔬 Ilmiy": [
        ("Astronomiya (10-11 sinf)","B. A. Vorontsov-Velyaminov","Koinot, sayyoralar, yulduzlar haqida to'liq ilmiy qo'llanma.","https://ziyouz.com/books/uzbek_darslik/astronomiya_10_11_sinf.pdf"),
        ("Fizika masalalari to'plami","I. Irodov","Oliy o'quv yurti uchun eng mashhur fizika masalalari.","https://archive.org/download/irodov-problems-general-physics/Irodov_Problems_in_General_Physics.pdf"),
        ("Umumiy kimyo","N. L. Glinka","Kimyoning barcha bo'limlari bo'yicha klassik universitetlik darslik.","https://archive.org/download/glinka-general-chemistry/Glinka_General_Chemistry.pdf"),
        ("Biologiya ensiklopediyasi","Turli mualliflar","Tirik organizmlar, genetika, ekologiya haqida qomuso'z.","https://ziyouz.com/books/uzbek_darslik/biologiya_ensiklopediya.pdf"),
        ("Oliy matematika","G. M. Fikhtengolts","Differensial va integral hisob bo'yicha eng to'liq darslik.","https://archive.org/download/fikhtengolts-calculus/Fikhtengolts_Calculus_Vol1.pdf"),
        ("Organik kimyo","R. Morrison, R. Boyd","Organik kimyoning klassik va eng keng qo'llaniluvchi darsligi.","https://archive.org/download/morrison-boyd-organic-chemistry/Morrison_Boyd_Organic_Chemistry.pdf"),
    ],
    "📗 Darslik": [
        ("Matematika 10-sinf","A. Abduhamidov va boshqalar","O'zbekiston umumta'lim maktablari uchun rasmiy darslik.","https://ziyouz.com/books/uzbek_darslik/matematika_10_sinf.pdf"),
        ("Ingliz tili grammatikasi","Raymond Murphy","English Grammar in Use — ingliz tilini o'rganuvchilar uchun.","https://archive.org/download/english-grammar-in-use-murphy/English_Grammar_in_Use_Murphy.pdf"),
        ("O'zbekiston tarixi 11-sinf","O'quv dasturi mualliflari","O'zbekiston tarixini to'liq qamrab oluvchi rasmiy maktab darsligi.","https://ziyouz.com/books/uzbek_darslik/ozbekiston_tarixi_11_sinf.pdf"),
        ("Ona tili va adabiyot 9-sinf","N. Mahkamov va boshqalar","O'zbek tili va adabiyotidan rasmiy maktab darsligi.","https://ziyouz.com/books/uzbek_darslik/ona_tili_9_sinf.pdf"),
        ("Fizika 9-sinf","S. Karimov va boshqalar","Mexanika, issiqlik, elektr bo'limlari bo'yicha maktab darsligi.","https://ziyouz.com/books/uzbek_darslik/fizika_9_sinf.pdf"),
        ("Kimyo 8-sinf","N. Nurmuxamedov va boshqalar","Kimyoning asosiy tushunchalari bo'yicha maktab darsligi.","https://ziyouz.com/books/uzbek_darslik/kimyo_8_sinf.pdf"),
    ],
    "💼 Biznes": [
        ("Boy dad kambag'al dad","Robert Kiyosaki","Moliyaviy erkinlik va investitsiya haqida dunyo bestselleri.","https://archive.org/download/rich-dad-poor-dad-uzbek/Rich_Dad_Poor_Dad_Uzbek.pdf"),
        ("Muvaffaqiyatli odamlarning 7 odati","Stephen Covey","Shaxsiy va kasbiy rivojlanish uchun zamonaviy klassika.","https://archive.org/download/7-habits-uzbek/7_Habits_Uzbek.pdf"),
        ("Noldan birga","Peter Thiel","Startup qurish va innovatsion biznes haqida amaliy qo'llanma.","https://archive.org/download/zero-to-one-uzbek/Zero_to_One_Uzbek.pdf"),
        ("Marketing menejment","Philip Kotler","Dunyo bo'yicha eng ko'p o'qiladigan marketing darsligi.","https://archive.org/download/kotler-marketing-management/Kotler_Marketing_Management.pdf"),
        ("Tez va sekin fikrlash","Daniel Kahneman","Nobel mukofoti sohibining inson qarorlariga oid asari.","https://archive.org/download/thinking-fast-slow-uzbek/Thinking_Fast_Slow_Uzbek.pdf"),
        ("Biznes o'yini","Oydin Mirzayev","O'zbek tadbirkorlar uchun yozilgan amaliy biznes qo'llanmasi.","https://ziyouz.com/books/uzbek_biznes/biznes_oyini.pdf"),
    ],
    "🧘 Psixologiya": [
        ("Do'st orttirish va odamlarga ta'sir etish","Dale Carnegie","Muloqot va liderlik bo'yicha 80 yillik world bestseller.","https://archive.org/download/how-to-win-friends-uzbek/How_To_Win_Friends_Uzbek.pdf"),
        ("Atom odatlar","James Clear","Kichik o'zgarishlar katta natijalarga qanday olib kelishini tushuntiradi.","https://archive.org/download/atomic-habits-uzbek/Atomic_Habits_Uzbek.pdf"),
        ("Hayotning ma'nosi","Viktor Frankl","Konslager tajribasidan chiqqan logoterapiya nazariyasi.","https://archive.org/download/mans-search-meaning-uzbek/Mans_Search_Meaning_Uzbek.pdf"),
        ("Emotsional intellekt","Daniel Goleman","IQ dan ko'ra muhimroq bo'lgan his-tuyg'ularni boshqarish san'ati.","https://archive.org/download/emotional-intelligence-uzbek/Emotional_Intelligence_Uzbek.pdf"),
        ("Fikrlash san'ati","Rolf Dobelli","Kundalik hayotdagi 52 xato fikrlash usullaridan qanday qutulish.","https://archive.org/download/art-of-thinking-clearly-uzbek/Art_Thinking_Clearly_Uzbek.pdf"),
        ("O'zingni o'zi anglash","Aziz Karimov","O'zbek psixolog tomonidan yozilgan shaxsiy rivojlanish kitobi.","https://ziyouz.com/books/uzbek_psixologiya/ozingni_anglash.pdf"),
    ],
    "💻 IT va Dasturlash": [
        ("Python bilan dasturlash","Al Sweigart","Automate the Boring Stuff — Python asoslari amaliy loyihalar bilan.","https://automatetheboringstuff.com/2e/chapter0/"),
        ("Toza kod (Clean Code)","Robert C. Martin","Sifatli, o'qilishi oson kod yozish bo'yicha professional standart.","https://archive.org/download/clean-code-robert-martin/Clean_Code_Robert_Martin.pdf"),
        ("Algoritmlar (CLRS)","Cormen, Leiserson, Rivest, Stein","Algoritmlar va ma'lumotlar tuzilmasi bo'yicha dunyo standarti darslik.","https://archive.org/download/introduction-to-algorithms-clrs/CLRS_Introduction_Algorithms.pdf"),
        ("Web dasturlash asoslari","Jon Duckett","HTML, CSS va JavaScript ni rasmlar bilan tushunarli o'rgatuvchi kitob.","https://archive.org/download/html-css-duckett/HTML_CSS_Duckett.pdf"),
        ("SQL to'liq qo'llanma","Alan Beaulieu","Ma'lumotlar bazasi va SQL so'rovlari bo'yicha amaliy darslik.","https://archive.org/download/learning-sql-beaulieu/Learning_SQL_Beaulieu.pdf"),
        ("Flutter bilan mobil dasturlash","Marco Napoli","Android va iOS uchun Flutter framework yordamida ilovalar yaratish.","https://archive.org/download/flutter-beginners-napoli/Flutter_Beginners_Napoli.pdf"),
    ],
}

UZBEK_NEWS = [
    {"sarlavha":"O'zbekiston iqtisodiyoti 2025 yilda 6.5 foizga o'sdi","manba":"kun.uz","url":"https://kun.uz","vaqt":"Bugun"},
    {"sarlavha":"Toshkentda yangi metro liniyasi qurilishi boshlandi","manba":"gazeta.uz","url":"https://gazeta.uz","vaqt":"Bugun"},
    {"sarlavha":"Prezident yangi ta'lim islohotlari farmonini imzoladi","manba":"uza.uz","url":"https://uza.uz","vaqt":"Bugun"},
    {"sarlavha":"O'zbekistonda turizm sohasi rekord darajaga yetdi","manba":"daryo.uz","url":"https://daryo.uz","vaqt":"Kecha"},
    {"sarlavha":"Samarqandda xalqaro investitsiya forumi muvaffaqiyatli o'tdi","manba":"kun.uz","url":"https://kun.uz","vaqt":"2 kun oldin"},
    {"sarlavha":"Yoshlar uchun yangi startup grantlari e'lon qilindi","manba":"gazeta.uz","url":"https://gazeta.uz","vaqt":"Bugun"},
    {"sarlavha":"O'zbekistonda yangi IT parklari va texnoparklar ochildi","manba":"it.uz","url":"https://it.uz","vaqt":"Kecha"},
    {"sarlavha":"Milliy futbol terma jamoamiz muhim g'alaba qozondi","manba":"sports.uz","url":"https://sports.uz","vaqt":"Bugun"},
    {"sarlavha":"O'zbekiston eksporti yangi tarixiy rekordga erishdi","manba":"uza.uz","url":"https://uza.uz","vaqt":"3 kun oldin"},
    {"sarlavha":"Toshkentda xalqaro madaniyat va san'at festivali ochildi","manba":"daryo.uz","url":"https://daryo.uz","vaqt":"Bugun"},
    {"sarlavha":"O'zbekistonda yangi zamonaviy shifoxonalar qurilmoqda","manba":"uza.uz","url":"https://uza.uz","vaqt":"Kecha"},
    {"sarlavha":"Respublikamizda qishloq xo'jaligini modernizatsiya qilish davom etmoqda","manba":"kun.uz","url":"https://kun.uz","vaqt":"2 kun oldin"},
]

WORLD_NEWS = [
    {"sarlavha":"Sun'iy intellekt texnologiyalari jahon iqtisodiyotini o'zgartirmoqda","manba":"BBC O'zbek","url":"https://bbc.com/uzbek","vaqt":"Bugun","kategoria":"💻 Texnologiya"},
    {"sarlavha":"Jahon banki rivojlanayotgan mamlakatlarga yangi kredit ajratdi","manba":"VOA O'zbek","url":"https://voanews.com/uzbek","vaqt":"Bugun","kategoria":"💼 Iqtisodiyot"},
    {"sarlavha":"Evropa Ittifoqi yangi energetika dasturini e'lon qildi","manba":"BBC O'zbek","url":"https://bbc.com/uzbek","vaqt":"Kecha","kategoria":"⚡ Energetika"},
    {"sarlavha":"NASA yangi kosmik missiyani muvaffaqiyatli yakunladi","manba":"Kun.uz xalqaro","url":"https://kun.uz","vaqt":"Bugun","kategoria":"🚀 Fan"},
    {"sarlavha":"Xitoy iqtisodiyoti o'sishda davom etmoqda","manba":"VOA O'zbek","url":"https://voanews.com/uzbek","vaqt":"2 kun oldin","kategoria":"💼 Iqtisodiyot"},
    {"sarlavha":"Yaqin Sharqda tinchlik muzokaralari qayta boshlandi","manba":"BBC O'zbek","url":"https://bbc.com/uzbek","vaqt":"Bugun","kategoria":"🌍 Siyosat"},
    {"sarlavha":"Jahon sog'liqni saqlash tashkiloti yangi tavsiyalar berdi","manba":"JSST","url":"https://who.int","vaqt":"Kecha","kategoria":"🏥 Salomatlik"},
    {"sarlavha":"Iqlim o'zgarishi bo'yicha xalqaro konferensiya bo'lib o'tdi","manba":"BBC O'zbek","url":"https://bbc.com/uzbek","vaqt":"3 kun oldin","kategoria":"🌱 Ekologiya"},
    {"sarlavha":"Jahon chempionatida kutilmagan natijalar qayd etildi","manba":"Sports.uz","url":"https://sports.uz","vaqt":"Bugun","kategoria":"⚽ Sport"},
    {"sarlavha":"Elektr avtomobillar bozori rekord savdoga erishdi","manba":"VOA O'zbek","url":"https://voanews.com/uzbek","vaqt":"Kecha","kategoria":"🚗 Transport"},
    {"sarlavha":"OpenAI yangi sun'iy intellekt modeli taqdim etdi","manba":"IT.uz","url":"https://it.uz","vaqt":"Bugun","kategoria":"💻 Texnologiya"},
    {"sarlavha":"G20 sammitida global iqtisodiyot masalalari muhokama qilindi","manba":"BBC O'zbek","url":"https://bbc.com/uzbek","vaqt":"2 kun oldin","kategoria":"🌍 Siyosat"},
]

MATH_TASKS = [
    ("2³ + √64 = ?","8 + 8 = 16"),("sin(90°) = ?","1"),("log₂(128) = ?","7"),
    ("(a+b)² = ?","a² + 2ab + b²"),("5! = ?","120"),("∫x²dx = ?","x³/3 + C"),
    ("π ≈ ?","3.14159265"),("12² - 5² = ?","119"),("√(16×25) = ?","20"),
    ("lim(x→0) sinx/x = ?","1"),("cos(0°) = ?","1"),("tan(45°) = ?","1"),
    ("2¹⁰ = ?","1024"),("e ≈ ?","2.71828"),("∑(1 to 100) = ?","5050"),
]

SCIENCE_FACTS = [
    "⚡ Chaqmoq 300,000 km/s tezlikda harakat qiladi","🧬 Inson DNKsi Quyoshgacha va qaytib yetadi",
    "🌍 Yer 4.5 milliard yil avval paydo bo'lgan","🫀 Yurak bir kunda 100,000 marta uradi",
    "🧠 Inson miyasi 100 milliard neyrondan iborat","🌊 Okean yer yuzasining 71 foizini qoplaydi",
    "☀️ Quyosh yorug'ligi Yerga 8 daqiqa 20 soniyada yetadi","🦴 Tug'ilganda 270 ta suyak, kattada 206 ta",
    "💧 Suv H₂O — 2 vodorod + 1 kislorod","🔬 Viruslar bakteriyalardan 10-100 marta kichik",
    "🌙 Oy Yerdan 384,400 km uzoqlikda joylashgan","🐘 Fil 22 oy davomida homilador bo'ladi",
    "🌡 Absolyut nol harorat: -273.15°C","💡 Yorug'lik 1 soniyada 7.5 marta Yer atrofini aylanadi",
    "🧪 Olmos — tabiatdagi eng qattiq modda",
]

LOGIC = [
    ("Qo'li bor lekin ishlamaydigan narsa nima?","⌚ Soat!"),
    ("100 dan 1 gacha sanasang nechta 9 bor?","20 ta!"),
    ("Inglizda eng ko'p ishlatiladigan harf?","E harfi"),
    ("12 tuxumdan 6 marta olinsa nechta qoladi?","0 ta — 6x2=12"),
    ("Suv tepaga chiqadigan joy qayer?","Quvur ichida!"),
    ("Yong'inni o'chirmay qo'yish uchun nima qilish kerak?","Yoqmaslik kerak!"),
    ("Eng uzun ingliz so'zi qaysi?","smiles — s va s orasida 1 mile bor!"),
]

SAYOHAT = {
    "🏙 Toshkent":{"joylar":["Xastimom masjidi","Chorsu bozori","Amir Temur xiyoboni","Teleminora","Eski shahar"],"taom":["Non kabob","Lagmon","Dimlama","Moshxo'rda","Somsa"],"maslahat":"Metro bilan harakat qilish qulay va arzon! 🚇","eng_yaxshi_vaqt":"Bahor va Kuz"},
    "🏛 Samarqand":{"joylar":["Registon maydoni","Shahi Zinda","Guri Amir","Bibi Xonim masjidi","Ulug'bek rasadxonasi"],"taom":["Samarqand noni","Shashlik","Somsa","Mastava","Naryn"],"maslahat":"Registon kechki yoritish shou — unutilmas taassurot! 🌟","eng_yaxshi_vaqt":"Aprel-May, Sentabr-Oktyabr"},
    "🕌 Buxoro":{"joylar":["Ark qal'asi","Kalon minorasi","Lyabi Hovuz","Chor Minor","Ismoil Somoniy maqbarasi"],"taom":["Buxoro oshi","Halim","Chuchvara","Qozonli go'sht"],"maslahat":"Kechqurun Lyabi Hovuz atrofida sayr — juda chiroyli! 🌙","eng_yaxshi_vaqt":"Mart-May, Sentyabr-Noyabr"},
    "🏰 Xiva":{"joylar":["Ichon Qal'a","Juma masjidi","Islam Xo'ja minorasi","Kunya Ark","Pahlavon Mahmud maqbarasi"],"taom":["Xorazm oshi","Shivit oshi","Gurvak","Mastava"],"maslahat":"UNESCO jahon merosi! Suratga olish uchun ideal. 📸","eng_yaxshi_vaqt":"Aprel-Iyun, Avgust-Oktyabr"},
    "🌿 Namangan":{"joylar":["Ota Valixon To'ra masjidi","Kosonsoy sharsharasi","Namangan bozori"],"taom":["Namangan somsa","Naryn","Qozon kabob","Chuchvara"],"maslahat":"O'zbekistonning 'bog' shahri — mevalar juda mazali! 🍑","eng_yaxshi_vaqt":"Iyul-Avgust (meva mavsumi)"},
    "🌄 Farg'ona":{"joylar":["Marg'ilon ipak fabrikasi","Rishton kulolchilik","Qo'qon xonligi saroyi"],"taom":["Farg'ona palov","Qozon kabob","Chuchvara","Lag'mon"],"maslahat":"Atlas ipak do'konlarini albatta ziyorat qiling! 🧵","eng_yaxshi_vaqt":"Bahor va Yoz"},
    "🏔 Andijon":{"joylar":["Jome masjidi","Bobur adabiyot muzeyi","Andijon bozori"],"taom":["Andijon palov","Somsa","Chuchvara","Mastava"],"maslahat":"Bobur vatanini ziyorat qiling — tarixiy shahar! 📜","eng_yaxshi_vaqt":"Bahor va Kuz"},
    "🌊 Urganch":{"joylar":["Al-Xorazmiy xiyoboni","Urganch bozori","Turobek Xonim maqbarasi"],"taom":["Xorazm oshi","Shivit oshi","Somsa","Mastava"],"maslahat":"Qadimiy Xorazm poytaxti — tarixi juda boy! 🏺","eng_yaxshi_vaqt":"Mart-May, Sentyabr-Oktyabr"},
    "🏔 Bishkek":{"joylar":["Ala-Too maydoni","Osh bozori","Manas haykali","Dordoy bozori"],"taom":["Beshbarmak","Lag'mon","Manty","Qimiz","Kurut"],"maslahat":"Osh bozorida milliy kiyim va xalq hunarmandchiligini ko'ring! 🛍","eng_yaxshi_vaqt":"Iyun-Sentyabr"},
    "🏕 Issiqko'l":{"joylar":["Issiqko'l ko'li","Cholpon-Ata","Karakol shahri","Jeti-Oguz qoyalari"],"taom":["Beshbarmak","Baliq taomi","Manty","Qimiz","Shorpo"],"maslahat":"Dunyo eng katta tog' ko'llaridan biri, suvi qish ham muzlamaydi! 💎","eng_yaxshi_vaqt":"Iyun-Avgust"},
    "🏙 Moskva":{"joylar":["Qizil maydon","Kreml","Arbat ko'chasi","Tretyakov galereyasi","Gorky parki"],"taom":["Borsh","Pelmeni","Beef Stroganoff","Blini","Shashlik"],"maslahat":"Metro — eng qulay transport, 1 kartada hamma joyga borasan! 🚇","eng_yaxshi_vaqt":"May-Sentyabr"},
    "🌆 Dubai":{"joylar":["Burj Khalifa","Dubai Mall","Palm Jumeirah","Dubai Creek","Desert Safari","Burj Al Arab"],"taom":["Shawarma","Al Machboos","Hummus","Falafel","Luqaimat"],"maslahat":"Ramazon oyida kiyim-kechakka e'tibor bering. Metro arzon va qulay! 🚇","eng_yaxshi_vaqt":"Noyabr-Mart"},
    "🕋 Makka":{"joylar":["Masjid al-Haram","Ka'ba","Zamzam qudug'i","Jabal al-Nur","Mina","Arafot"],"taom":["Kabsa","Mandi","Shawarma","Mutabbaq","Xurmo"],"maslahat":"Faqat musulmonlar kirishi mumkin. Haj va Umra uchun oldindan ruxsat oling! 🤲","eng_yaxshi_vaqt":"Yil davomida"},
    "🗽 Nyu-York":{"joylar":["Ozodlik haykali","Central Park","Times Square","Brooklyn ko'prigi","Empire State Building"],"taom":["New York pizza","Hot dog","Cheesecake","Bagel","Buffalo wings"],"maslahat":"Metro 24/7 ishlaydi. MetroCard olish eng iqtisodiy variant! 🚇","eng_yaxshi_vaqt":"Aprel-Iyun, Sentyabr-Noyabr"},
    "🎬 Los-Anjeles":{"joylar":["Hollywood","Disneyland","Santa Monica Beach","Universal Studios","Getty Center"],"taom":["In-N-Out burger","Fish tacos","Avocado toast","Korean BBQ","Sushi"],"maslahat":"Mashina ijaraga olish shart — jamoat transporti yaxshi emas! 🚗","eng_yaxshi_vaqt":"Mart-May, Sentyabr-Noyabr"},
}

SOS_DATA = {
    "sos_med": "🏥 *TEZ YORDAM*\n━━━━━━━━━━━━━━━━━━━━\n\n📞 *103* — Tez tibbiy yordam\n📞 *1003* — Xususiy tez yordam\n\n⚠️ *Nima qilish kerak:*\n• Nafas olmasa — sun'iy nafas bering\n• Qon ketsa — bosib to'xtating\n• Harakatsiz qolsa — siljitmang\n• Aniq manzilni ayting!\n━━━━━━━━━━━━━━━━━━━━",
    "sos_fire": "🚒 *YONG'IN XIZMATI*\n━━━━━━━━━━━━━━━━━━━━\n\n📞 *101* — Yong'in o'chirish\n\n⚠️ *Yong'inda nima qilish:*\n• Darhol binoni tark eting\n• Lift ishlatmang — zinapoyadan!\n• Tutun bo'lsa — egilib yuring\n• Eshikni yopib chiqing\n━━━━━━━━━━━━━━━━━━━━",
    "sos_police": "👮 *POLITSIYA*\n━━━━━━━━━━━━━━━━━━━━\n\n📞 *102* — Politsiya\n📞 *1102* — Yo'l politsiyasi\n\n⚠️ *Maslahatlar:*\n• Tinch turing, vahima qilmang\n• Aniq manzil va holat ayting\n• Hujjatlashtiring (foto/video)\n━━━━━━━━━━━━━━━━━━━━",
    "sos_emergency": "🌊 *FAVQULODDA VAZIYATLAR*\n━━━━━━━━━━━━━━━━━━━━\n\n📞 *1050* — FVV xizmati\n📞 *112* — Yagona xizmat\n\n⚠️ *Zilzila bo'lsa:*\n• Stol ostiga yashiring\n• Devordan uzoqda turing\n• Liftdan foydalanmang\n\n⚠️ *Sel bo'lsa:*\n• Yuqori joyga ko'tariling\n• Suvli yo'ldan o'tmang\n━━━━━━━━━━━━━━━━━━━━",
    "sos_all": "☎️ *BARCHA MUHIM RAQAMLAR*\n━━━━━━━━━━━━━━━━━━━━\n\n🏥 Tez yordam:       *103*\n🚒 Yong'in:           *101*\n👮 Politsiya:         *102*\n🌊 FVV:               *1050*\n📞 Yagona:            *112*\n🚗 Yo'l politsiyasi:  *1102*\nℹ️ Ma'lumotnoma:     *109*\n🏦 Bank xizmati:      *1007*\n━━━━━━━━━━━━━━━━━━━━\n🔋 _Telefon o'chib borayotganda — faqat *112* ga qo'ng'iroq qiling!_",
}


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(KeyboardButton("🌦 Ob-havo"), KeyboardButton("💱 Valyuta kursi"))
    markup.row(KeyboardButton("📰 Yangiliklar"), KeyboardButton("📊 Kripto narxlari"))
    markup.row(KeyboardButton("📚 Kitoblar"), KeyboardButton("🧩 O'quv mashqlari"))
    markup.row(KeyboardButton("🧭 Sayohat"), KeyboardButton("🚨 SOS"))
    return markup


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


@bot.message_handler(func=lambda m: m.text == "🌦 Ob-havo")
def weather_region(message):
    user_states[message.chat.id] = "weather_region"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for viloyat in HUDUDLAR.keys():
        markup.add(KeyboardButton(viloyat))
    markup.add(KeyboardButton("🔙 Orqaga"))
    bot.send_message(message.chat.id, "🗺 *Viloyatni tanlang:*", parse_mode="Markdown", reply_markup=markup)


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
    bot.send_message(message.chat.id, f"📍 *{viloyat}*\n🏘 Tumanni tanlang:", parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "weather_district")
def weather_show(message):
    if "Viloyatga qaytish" in message.text:
        user_states[message.chat.id] = "weather_region"
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for viloyat in HUDUDLAR.keys():
            markup.add(KeyboardButton(viloyat))
        markup.add(KeyboardButton("🔙 Orqaga"))
        bot.send_message(message.chat.id, "🗺 *Viloyatni tanlang:*", parse_mode="Markdown", reply_markup=markup)
        return
    tuman = message.text.strip()
    viloyat = user_data.get(message.chat.id, {}).get("viloyat", "")
    user_states[message.chat.id] = None
    bot.send_message(message.chat.id, f"⏳ *{tuman}* ob-havosi yuklanmoqda...", parse_mode="Markdown")
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={tuman},UZ&appid={WEATHER_API_KEY}&units=metric&lang=en"
        r = requests.get(url, timeout=10)
        d = r.json()
        if d.get("cod") == 200:
            temp = d["main"]["temp"]
            feels = d["main"]["feels_like"]
            humidity = d["main"]["humidity"]
            wind = d["wind"]["speed"]
            pressure = d["main"]["pressure"]
            desc_en = d["weather"][0]["description"].lower()
            desc_uz = OB_HAVO_UZ.get(desc_en, desc_en.capitalize())
            w_id = d["weather"][0]["id"]
            if w_id == 800: icon = "☀️"
            elif 801 <= w_id <= 804: icon = "⛅"
            elif w_id < 300: icon = "⛈"
            elif w_id < 400: icon = "🌦"
            elif w_id < 600: icon = "🌧"
            elif w_id < 700: icon = "❄️"
            else: icon = "🌫"
            if temp >= 35: t_baho = "🥵 Juda issiq"
            elif temp >= 25: t_baho = "☀️ Issiq"
            elif temp >= 15: t_baho = "😊 Iliq"
            elif temp >= 5: t_baho = "🧥 Salqin"
            elif temp >= 0: t_baho = "🥶 Sovuq"
            else: t_baho = "❄️ Qattiq sovuq"
            text = (
                f"{icon} *{tuman} Ob-Havosi*\n📍 _{viloyat}_\n"
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
            url2 = f"https://api.openweathermap.org/data/2.5/weather?q={viloyat_nomi},UZ&appid={WEATHER_API_KEY}&units=metric&lang=en"
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


@bot.message_handler(func=lambda m: m.text == "💱 Valyuta kursi")
def currency(message):
    bot.send_message(message.chat.id, "⏳ Valyuta kurslari yuklanmoqda...")
    try:
        url = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.encoding = "utf-8"
        data = r.json()
        SHOW = {"USD":"🇺🇸","EUR":"🇪🇺","RUB":"🇷🇺","GBP":"🇬🇧","JPY":"🇯🇵","CNY":"🇨🇳","KZT":"🇰🇿","KRW":"🇰🇷","TRY":"🇹🇷","AED":"🇦🇪","SAR":"🇸🇦","GEL":"🇬🇪"}
        text = f"💱 *Markaziy Bank Valyuta Kurslari*\n📅 {datetime.now().strftime('%d.%m.%Y')}\n━━━━━━━━━━━━━━━━━━━━\n\n"
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
        bot.send_message(message.chat.id, f"⚠️ Xatolik: `{e}`", parse_mode="Markdown", reply_markup=main_menu())


@bot.message_handler(func=lambda m: m.text == "📰 Yangiliklar")
def news_menu(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🇺🇿 O'zbek yangiliklari", callback_data="news_uz"),
        InlineKeyboardButton("🌍 Dunyo yangiliklari", callback_data="news_world")
    )
    bot.send_message(message.chat.id, "📰 *Qaysi yangiliklar?*", parse_mode="Markdown", reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data.startswith("news_"))
def news_fetch(call):
    bot.answer_callback_query(call.id, "⏳ Yuklanmoqda...")
    cid = call.message.chat.id
    if call.data == "news_uz":
        news_list = random.sample(UZBEK_NEWS, min(6, len(UZBEK_NEWS)))
        text = f"📰 *O'zbekiston Yangiliklari*\n📅 {datetime.now().strftime('%d.%m.%Y  %H:%M')}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for i, n in enumerate(news_list, 1):
            text += f"*{i}.* {n['sarlavha']}\n   🗞 _{n['manba']}_  •  🕐 _{n['vaqt']}_\n   🔗 [Batafsil o'qish]({n['url']})\n\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n📌 *To'liq yangiliklar:*\n[kun.uz](https://kun.uz) • [gazeta.uz](https://gazeta.uz)\n[daryo.uz](https://daryo.uz) • [uza.uz](https://uza.uz)"
    else:
        news_list = random.sample(WORLD_NEWS, min(6, len(WORLD_NEWS)))
        text = f"🌍 *Dunyo Yangiliklari*\n📅 {datetime.now().strftime('%d.%m.%Y  %H:%M')}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for i, n in enumerate(news_list, 1):
            text += f"*{i}.* {n['kategoria']}\n   {n['sarlavha']}\n   🗞 _{n['manba']}_  •  🕐 _{n['vaqt']}_\n   🔗 [Batafsil o'qish]({n['url']})\n\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n📌 *To'liq xalqaro yangiliklar:*\n[BBC O'zbek](https://bbc.com/uzbek) • [VOA O'zbek](https://voanews.com/uzbek)"
    bot.send_message(cid, text, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=main_menu())


@bot.message_handler(func=lambda m: m.text == "📊 Kripto narxlari")
def crypto(message):
    bot.send_message(message.chat.id, "⏳ Kripto narxlar yuklanmoqda...")
    try:
        ids = "bitcoin,ethereum,binancecoin,solana,toncoin,ripple,cardano,dogecoin,polkadot,avalanche-2"
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        data = r.json()
        COINS = [
            ("bitcoin","₿","Bitcoin","BTC"),("ethereum","Ξ","Ethereum","ETH"),
            ("binancecoin","🔶","BNB","BNB"),("solana","◎","Solana","SOL"),
            ("toncoin","💎","TON","TON"),("ripple","💧","XRP","XRP"),
            ("cardano","🔵","Cardano","ADA"),("dogecoin","🐕","Dogecoin","DOGE"),
            ("polkadot","⚪","Polkadot","DOT"),("avalanche-2","🔺","Avalanche","AVAX"),
        ]
        text = f"📊 *Kripto Valyuta Narxlari*\n🕐 {datetime.now().strftime('%H:%M  |  %d.%m.%Y')}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for cid_c, icon, name, sym in COINS:
            if cid_c in data:
                price = data[cid_c].get("usd", 0)
                change = data[cid_c].get("usd_24h_change", 0)
                arrow = "📈" if change >= 0 else "📉"
                p_str = f"${price:,.2f}" if price >= 1 else f"${price:.5f}"
                text += f"{icon} *{name}* `{sym}`\n   💵 {p_str}   {arrow} `{change:+.2f}%`\n\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n🔗 _Manba: CoinGecko_"
        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Xatolik: `{e}`", parse_mode="Markdown", reply_markup=main_menu())


@bot.message_handler(func=lambda m: m.text == "📚 Kitoblar")
def books_menu(message):
    user_states[message.chat.id] = "books"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for k in KITOB_MENU:
        markup.add(KeyboardButton(k))
    markup.add(KeyboardButton("🔙 Orqaga"))
    bot.send_message(message.chat.id, "📚 *Kitob turini tanlang:*", parse_mode="Markdown", reply_markup=markup)


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
        bot.send_message(message.chat.id, f"⏳ *{tur}* kitoblari tayyorlanmoqda...", parse_mode="Markdown")
        zip_path = os.path.join(TEMP_DIR, f"pixo_kitoblar_{message.chat.id}.zip")
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for i, (nom, muallif, tavsif, havola) in enumerate(KITOBLAR[tur], 1):
                    content = (
                        f"╔══════════════════════════════════════╗\n"
                        f"         📚 PIXO BOT KUTUBXONASI\n"
                        f"╚══════════════════════════════════════╝\n\n"
                        f"📖 Kitob nomi : {nom}\n✍️  Muallif    : {muallif}\n"
                        f"📝 Tavsif     : {tavsif}\n📂 Kategoriya : {tur}\n\n"
                        f"{'='*42}\n          🔗 YUKLAB OLISH HAVOLALARI\n{'='*42}\n\n"
                        f"✅ TO'G'RIDAN-TO'G'RI HAVOLA:\n   {havola}\n\n"
                        f"{'─'*42}\n\n📌 QO'SHIMCHA SAYTLAR:\n\n"
                        f"1. Ziyouz.com: https://ziyouz.com\n"
                        f"2. Z-Library: https://z-lib.org\n"
                        f"3. Archive.org: https://archive.org/search?query={nom.replace(' ', '+')}\n"
                        f"4. PDF Drive: https://www.pdfdrive.com/search?q={nom.replace(' ', '+')}\n\n"
                        f"{'='*42}\n🤖 Pixo Bot | 📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                    )
                    safe = f"{i:02d}_{nom[:25].replace('/', '_').replace(':', '_')}.txt"
                    zf.writestr(safe, content)
                readme = (
                    f"📚 PIXO BOT — {tur.upper()} KITOBLARI\n{'='*42}\n\n"
                    f"Bu ZIP faylda {len(KITOBLAR[tur])} ta kitob havolasi mavjud.\n\n"
                    f"BEPUL SAYTLAR:\n• ziyouz.com\n• z-lib.org\n• archive.org\n• pdfdrive.com\n\n"
                    f"🤖 Pixo Bot | {datetime.now().strftime('%d.%m.%Y')}\n"
                )
                zf.writestr("00_README.txt", readme)
            list_text = f"📚 *{tur}* kitoblari:\n━━━━━━━━━━━━━━━━━━━━\n\n"
            for i, (nom, muallif, tavsif, _) in enumerate(KITOBLAR[tur], 1):
                list_text += f"  *{i}.* {nom}\n      _✍️ {muallif}_\n      _{tavsif}_\n\n"
            list_text += "━━━━━━━━━━━━━━━━━━━━\n📦 ZIP yuborilmoqda..."
            bot.send_message(message.chat.id, list_text, parse_mode="Markdown")
            with open(zip_path, "rb") as f:
                bot.send_document(message.chat.id, f,
                    caption=f"📚 *{tur}*\n━━━━━━━━━━━━━━━━━━━━\n📁 {len(KITOBLAR[tur])} ta kitob + README\n💡 Har bir faylda to'g'ridan-to'g'ri havola bor",
                    parse_mode="Markdown")
            if os.path.exists(zip_path):
                os.remove(zip_path)
            bot.send_message(message.chat.id, "✅ *Muvaffaqiyatli yuborildi!*", parse_mode="Markdown", reply_markup=main_menu())
        except Exception as e:
            if os.path.exists(zip_path):
                try: os.remove(zip_path)
                except: pass
            fallback = f"📚 *{tur}* kitoblari:\n━━━━━━━━━━━━━━━━━━━━\n\n"
            for i, (nom, muallif, tavsif, havola) in enumerate(KITOBLAR[tur], 1):
                fallback += f"*{i}. {nom}*\n✍️ _{muallif}_\n📝 _{tavsif}_\n🔗 [Yuklab olish]({havola})\n\n"
            fallback += "━━━━━━━━━━━━━━━━━━━━\n📌 *Bepul kutubxonalar:*\n• [Ziyouz.com](https://ziyouz.com)\n• [Z-Library](https://z-lib.org)\n• [PDF Drive](https://pdfdrive.com)"
            bot.send_message(message.chat.id, fallback, parse_mode="Markdown", disable_web_page_preview=False, reply_markup=main_menu())
    else:
        user_states[message.chat.id] = "books"
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for k in KITOB_MENU:
            markup.add(KeyboardButton(k))
        markup.add(KeyboardButton("🔙 Orqaga"))
        bot.send_message(message.chat.id, "❌ Tugmani bosing:", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "🧩 O'quv mashqlari")
def edu_menu(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🧮 Matematika", callback_data="edu_math"),
        InlineKeyboardButton("🔬 Ilmiy faktlar", callback_data="edu_science"),
        InlineKeyboardButton("🧠 Mantiq o'yini", callback_data="edu_logic"),
        InlineKeyboardButton("💻 IT kurslar", callback_data="edu_it"),
        InlineKeyboardButton("🗣 Til o'rganish", callback_data="edu_lang"),
        InlineKeyboardButton("📅 Dars jadvali", callback_data="edu_schedule"),
    )
    bot.send_message(message.chat.id, "🧩 *O'quv Mashqlari*\n━━━━━━━━━━━━━━━━━━━━\nNimani o'rganasiz?", parse_mode="Markdown", reply_markup=markup)


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
        text = f"🧠 *Mantiq O'yini*\n━━━━━━━━━━━━━━━━━━━━\n\n❓ *Savol:*\n_{q}_\n\n||✅ *Javob:* {a}||"
    elif d == "edu_it":
        text = ("💻 *IT Kurslar va Resurslar*\n━━━━━━━━━━━━━━━━━━━━\n\n"
                "🐍 *Python:*\n   [python.org](https://python.org)\n\n"
                "🌐 *Web:*\n   [freecodecamp.org](https://freecodecamp.org)\n\n"
                "📱 *Flutter:*\n   [flutter.dev](https://flutter.dev)\n\n"
                "🤖 *ML/AI:*\n   [coursera.org](https://coursera.org)\n\n"
                "🛢 *SQL:*\n   [sqlzoo.net](https://sqlzoo.net)\n\n"
                "📺 *O'zbek kanallar:*\n   IT Park Uzbekistan")
    elif d == "edu_lang":
        text = ("🗣 *Til O'rganish Resurslari*\n━━━━━━━━━━━━━━━━━━━━\n\n"
                "🇬🇧 *Ingliz:*\n   [duolingo.com](https://duolingo.com)\n\n"
                "🇷🇺 *Rus:*\n   [russiapod101.com](https://russiapod101.com)\n\n"
                "🇩🇪 *Nemis:*\n   [dw.com](https://dw.com/en/learn-german)\n\n"
                "🇰🇷 *Koreys:*\n   [talktomeinkorean.com](https://talktomeinkorean.com)\n\n"
                "🇨🇳 *Xitoy:*\n   [hellochinese.com](https://hellochinese.com)\n\n"
                "🇦🇪 *Arab:*\n   [arabicpod101.com](https://arabicpod101.com)")
    elif d == "edu_schedule":
        text = ("📅 *Kunlik Dars Jadvali*\n━━━━━━━━━━━━━━━━━━━━\n\n"
                "🌅 `07:00` — Uyg'onish + mashq\n📖 `08:00` — Asosiy fanlar\n"
                "☕ `10:00` — Dam olish\n💻 `10:15` — Dasturlash\n"
                "🍽 `12:00` — Tushlik\n🗣 `13:00` — Til o'rganish\n"
                "📚 `15:00` — Uy vazifasi\n🏃 `17:00` — Sport\n"
                "🔬 `19:00` — Ilmiy fanlar\n🌙 `22:00` — Uyqu\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "💡 _Har kuni 1% yaxshilansang — 1 yilda 37 marta o'sasan!_ 🚀")
    else:
        text = "❌ Noma'lum"
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())


@bot.message_handler(func=lambda m: m.text == "🧭 Sayohat")
def travel_menu(message):
    user_states[message.chat.id] = "travel"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for city in SAYOHAT.keys():
        markup.add(KeyboardButton(city))
    markup.add(KeyboardButton("🔙 Orqaga"))
    bot.send_message(message.chat.id, "✈️ *Qaysi shaharga borasiz?*", parse_mode="Markdown", reply_markup=markup)


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
            f"✈️ *{found}*\n━━━━━━━━━━━━━━━━━━━━\n\n"
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


@bot.message_handler(func=lambda m: m.text == "🚨 SOS")
def sos(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🏥 Tez yordam", callback_data="sos_med"),
        InlineKeyboardButton("🚒 Yong'in", callback_data="sos_fire"),
        InlineKeyboardButton("👮 Politsiya", callback_data="sos_police"),
        InlineKeyboardButton("🌊 Favqulodda", callback_data="sos_emergency"),
        InlineKeyboardButton("☎️ Barcha raqamlar", callback_data="sos_all"),
    )
    bot.send_message(message.chat.id, "🚨 *FAVQULODDA YORDAM*\n━━━━━━━━━━━━━━━━━━━━\n❗ Qanday yordam kerak?", parse_mode="Markdown", reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data.startswith("sos_"))
def sos_callback(call):
    bot.answer_callback_query(call.id)
    text = SOS_DATA.get(call.data, "❌ Topilmadi")
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())


@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(message.chat.id, "❓ *Tushunmadim.*\nQuyidagi menyudan tanlang 👇", parse_mode="Markdown", reply_markup=main_menu())


# ==================== FLASK ROUTES ====================

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "✅ Pixo Bot ishlamoqda!", 200

@app.route("/set_webhook")
def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    bot.remove_webhook()
    result = bot.set_webhook(url=webhook_url)
    if result:
        return f"✅ Webhook o'rnatildi: {webhook_url}", 200
    else:
        return "❌ Webhook o'rnatishda xatolik", 500


# ==================== ISHGA TUSHIRISH ====================

if WEBHOOK_URL:
    webhook_full = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_full)
