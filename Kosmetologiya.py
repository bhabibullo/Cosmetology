import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from asyncio import run
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

bot_token = ""
bot = Bot(token=bot_token)
dp = Dispatcher()

admin_id = 6458736545
channel_id = -1002367748942
CHANNEL_ID = ""

LANGUAGES = {
    'uz': 'Ozbek 🇺🇿',
    'ru': 'Русский 🇷🇺',
    'en': 'English 🇬🇧'
}

BASE_COSMETOLOGISTS = {
    "Madina": {
        'uz': "Madina Karimova",
        'ru': "Мадина Каримова",
        'en': "Madina Karimova"
    },
    "Dildora": {
        'uz': "Dildora Rixsibayeva",
        'ru': "Дилдора Рихсибаева",
        'en': "Dildora Rikhsibayeva"
    },
    "Sabina": {
        'uz': "Sabina Aliyeva",
        'ru': "Сабина Алиева",
        'en': "Sabina Aliyeva"
    },
    "Nilufar": {
        'uz': "Nilufar Rahimova",
        'ru': "Нилуфар Рахимова",
        'en': "Nilufar Rakhimova"
    },
    "Shahzoda": {
        'uz': "Shahzoda Umarova",
        'ru': "Шахзода Умарова",
        'en': "Shahzoda Umarova"
    }
}

cosmetologists = {
    'uz': ["Madina Karimova", "Dildora Rixsibayeva", "Sabina Aliyeva", "Nilufar Rahimova", "Shahzoda Umarova"],
    'ru': ["Мадина Каримова", "Дилдора Рихсибаева", "Сабина Алиева", "Нилуфар Рахимова", "Шахзода Умарова"],
    'en': ["Madina Karimova", "Dildora Rikhsibayeva", "Sabina Aliyeva", "Nilufar Rakhimova", "Shahzoda Umarova"]
}

hair_types = {
    'uz': {
        'simple': {
            'display': 'Oddiy soch turmagi',
            'duration': 60  # 1 soat
        },
        'evening': {
            'display': 'Kechki soch turmagi',
            'duration': 90  # 1.5 soat
        },
        'wedding': {
            'display': 'To\'y soch turmagi',
            'duration': 120  # 2 soat
        }
    },
    'ru': {
        'simple': {
            'display': 'Простая причёска',
            'duration': 60
        },
        'evening': {
            'display': 'Вечерняя причёска',
            'duration': 90
        },
        'wedding': {
            'display': 'Свадебная причёска',
            'duration': 120
        }
    },
    'en': {
        'simple': {
            'display': 'Simple hairstyle',
            'duration': 60
        },
        'evening': {
            'display': 'Evening hairstyle',
            'duration': 90
        },
        'wedding': {
            'display': 'Wedding hairstyle',
            'duration': 120
        }
    }
}

texts = {
    'uz': {
        'welcome': "Xush kelibsiz! Tilni tanlang:",
        'start': "Xush kelibsiz! Tilni tanlang:",
        'enter_name': "Ismingizni kiriting:",
        'enter_phone': "Telefon raqamingizni yuboring:",
        'share_contact': "Telefon raqamni yuborish",
        'share_number': "📱 Telefon raqamni yuborish",
        'select_cosmetologist': "Kosmetologni tanlang:",
        'select_hair_type': "Xizmat turini tanlang:",
        'select_date': "Sanani tanlang:",
        'select_time': "Vaqtni tanlang:",
        'available_times': "Mavjud vaqtlar:",
        'time_booked': "Bu vaqt band qilingan!",
        'confirm_booking': "Quyidagi ma'lumotlarni tasdiqlaysizmi?",
        'yes': "✅ Ha",
        'no': "❌ Yo'q",
        'booking_confirmed': "Buyurtmangiz tasdiqlandi!\n\nBatafsil ma\'lumotlar:",
        'booking_cancelled': "Buyurtma bekor qilindi.",
        'new_booking': '🔄 Yangi buyurtma'
    },
    'ru': {
        'welcome': "Добро пожаловать! Выберите язык:",
        'start': "Добро пожаловать! Выберите язык:",
        'enter_name': "Введите ваше имя:",
        'enter_phone': "Отправьте ваш номер телефона:",
        'share_contact': "Отправить номер телефона",
        'share_number': "📱 Поделиться номером",
        'select_cosmetologist': "Выберите косметолога:",
        'select_hair_type': "Выберите тип услуги:",
        'select_date': "Выберите дату:",
        'select_time': "Выберите время:",
        'available_times': "Доступное время:",
        'time_booked': "Это время уже занято!",
        'confirm_booking': "Подтверждаете следующие данные?",
        'yes': "✅ Да",
        'no': "❌ Нет",
        'booking_confirmed': "Ваша запись подтверждена!\n\nПодробная информация:",
        'booking_cancelled': "Запись отменена.",
        'new_booking': '🔄 Новая запись'
    },
    'en': {
        'welcome': "Welcome! Choose language:",
        'start': "Welcome! Choose language:",
        'enter_name': "Enter your name:",
        'enter_phone': "Send your phone number:",
        'share_contact': "Share phone number",
        'share_number': "📱 Share phone number",
        'select_cosmetologist': "Select cosmetologist:",
        'select_hair_type': "Select service type:",
        'select_date': "Select date:",
        'select_time': "Select time:",
        'available_times': "Available times:",
        'time_booked': "This time is already booked!",
        'confirm_booking': "Do you confirm the following details?",
        'yes': "✅ Yes",
        'no': "❌ No",
        'booking_confirmed': "Your booking is confirmed!\n\nDetails:",
        'booking_cancelled': "Booking cancelled.",
        'new_booking': '🔄 New booking'
    }
}

months = {
    'uz': {
        1: "Yanvar", 2: "Fevral", 3: "Mart", 4: "Aprel", 5: "May", 6: "Iyun",
        7: "Iyul", 8: "Avgust", 9: "Sentabr", 10: "Oktabr", 11: "Noyabr", 12: "Dekabr"
    },
    'ru': {
        1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
        7: "Июь", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    },
    'en': {
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
    }
}

user_data = {}
selected_language = {}
selected_cosmetologist = {}
selected_hair_type = {}
selected_date = {}
selected_time = {}

# Kosmetologlar jadvali
COSMETOLOGISTS_SCHEDULE = {
    "Madina": {
        "name": "Madina Karimova",
        "work_hours": {"start": "09:00", "end": "21:00"},
        "appointments": {}
    },
    "Dildora": {
        "name": "Dildora Rixsibayeva",
        "work_hours": {"start": "09:00", "end": "21:00"},
        "appointments": {}
    },
    "Sabina": {
        "name": "Sabina Aliyeva",
        "work_hours": {"start": "09:00", "end": "21:00"},
        "appointments": {}
    }
}

def time_to_minutes(time_str):
    """Vaqtni daqiqalarga o'tkazish"""
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def minutes_to_time(minutes):
    """Daqiqalarni vaqt formatiga o'tkazish"""
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02d}:{minutes:02d}"

def get_available_slots(cosmetologist, date, duration):
    """Bo'sh vaqtlarni hisoblash"""
    schedule = COSMETOLOGISTS_SCHEDULE[cosmetologist]
    work_start = time_to_minutes(schedule["work_hours"]["start"])  # 9:00 = 540 daqiqa
    work_end = time_to_minutes(schedule["work_hours"]["end"])      # 21:00 = 1260 daqiqa
    
    # Band vaqtlarni olish va saralash
    appointments = schedule["appointments"].get(date, [])
    appointments.sort(key=lambda x: time_to_minutes(x[0]))
    
    available_slots = []
    current_time = work_start
    
    # Xizmat davomiyligiga qarab slot yaratish
    while current_time + duration <= work_end:
        is_available = True
        
        # Band vaqtlar bilan tekshirish
        for start, end in appointments:
            if (current_time < time_to_minutes(end) and 
                current_time + duration > time_to_minutes(start)):
                is_available = False
                current_time = time_to_minutes(end)  # Band vaqt tugashigacha o'tkazib yuborish
                break
        
        if is_available:
            start_time = minutes_to_time(current_time)
            end_time = minutes_to_time(current_time + duration)
            available_slots.append((start_time, end_time))
            current_time += duration  # Xizmat davomiyligiga qarab keyingi vaqtga o'tish
        else:
            continue
    
    return available_slots

def generate_dates(lang):
    """Keyingi 7 kun uchun sanalarni yaratish"""
    dates = []
    months = {
        'uz': ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 
               'Avgust', 'Sentabr', 'Oktabr', 'Noyabr', 'Dekabr'],
        'ru': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
               'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']
    }
    
    weekdays = {
        'uz': ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba'],
        'ru': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
        'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
    
    current_date = datetime.now()
    
    # Bugundan boshlab 7 kun
    for i in range(7):
        date = current_date + timedelta(days=i)
        weekday = weekdays[lang][date.weekday()]
        
        # Bugun va ertaga uchun maxsus ko'rsatish
        if i == 0:
            display_date = f"Bugun, {date.day}-{months[lang][date.month-1]}"
            if lang == 'ru':
                display_date = f"Сегодня, {date.day}-{months[lang][date.month-1]}"
            elif lang == 'en':
                display_date = f"Today, {date.day}-{months[lang][date.month-1]}"
        elif i == 1:
            display_date = f"Ertaga, {date.day}-{months[lang][date.month-1]}"
            if lang == 'ru':
                display_date = f"Завтра, {date.day}-{months[lang][date.month-1]}"
            elif lang == 'en':
                display_date = f"Tomorrow, {date.day}-{months[lang][date.month-1]}"
        else:
            display_date = f"{weekday}, {date.day}-{months[lang][date.month-1]}"
        
        callback_date = f"{i+1}-{date.strftime('%Y-%m-%d')}"
        dates.append((display_date, callback_date))
    
    return dates

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    
    # Foydalanuvchi ma'lumotlarini boshlang'ich holatga keltirish
    user_data[user_id] = {
        "language": "uz",  # Standart til
        "name": None,
        "phone": None
    }
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
        ]
    ])
    
    await message.answer(texts['uz']['welcome'], reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith('lang_'))
async def language_selected(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = callback_query.data.split('_')[1]
    selected_language[user_id] = lang
    user_data[user_id] = {"step": "name", "language": lang}
    
    await callback_query.message.edit_text(texts[lang]['enter_name'])

@dp.message(lambda message: message.text and message.from_user.id in user_data and user_data[message.from_user.id]["step"] == "name")
async def process_name(message: types.Message):

    user_id = message.from_user.id
    lang = user_data[user_id]["language"]
    user_data[user_id]["name"] = message.text
    user_data[user_id]["step"] = "phone"
    
    share_button = KeyboardButton(text=texts[lang]['share_number'], request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[share_button]], resize_keyboard=True)
    await message.answer(texts[lang]['enter_phone'], reply_markup=keyboard)

@dp.message(lambda message: message.contact or message.text)
async def process_phone(message: types.Message):
    user_id = message.from_user.id
    
    # Foydalanuvchi ma'lumotlari mavjudligini tekshirish
    if user_id not in user_data or "step" not in user_data[user_id] or user_data[user_id]["step"] != "phone":
        return
    
    lang = user_data[user_id]["language"]
    
    # Telefon raqamni olish (contact orqali yoki matn ko'rinishida)
    if message.contact:
        user_data[user_id]["phone"] = message.contact.phone_number
    else:
        # Raqamni tozalash (faqat raqamlarni qoldirish)
        phone = ''.join(filter(str.isdigit, message.text))
        if phone:  # Agar raqam mavjud bo'lsa
            user_data[user_id]["phone"] = phone
        else:
            return  # Agar raqam topilmasa, funksiyadan chiqish
    
    # Tugmalarni olib tashlash
    remove_keyboard = ReplyKeyboardRemove()
    
    # Kosmetologlarni ko'rsatish
    cosmetologist_buttons = []
    row = []
    for cosmetologist_id, cosmetologist in enumerate(COSMETOLOGISTS_SCHEDULE.items()):
        name = cosmetologist[1]["name"]
        button = InlineKeyboardButton(
            text=name,
            callback_data=f"cosmetologist_{cosmetologist[0]}"
        )
        row.append(button)
        if len(row) == 2 or cosmetologist_id == len(COSMETOLOGISTS_SCHEDULE) - 1:
            cosmetologist_buttons.append(row)
            row = []
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=cosmetologist_buttons)
    
    # Avval tugmalarni olib tashlaymiz, keyin yangi xabarni yuboramiz
    await message.answer(texts[lang]['select_cosmetologist'], 
                        reply_markup=remove_keyboard)
    await message.answer(texts[lang]['select_cosmetologist'], 
                        reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith('cosmetologist_'))
async def cosmetologist_selected(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = user_data[user_id]["language"]
    
    # Kosmetolog nomini olish
    selected_cosmetologist[user_id] = callback_query.data.split('_')[1]
    
    # Soch turlarini ko'rsatish
    hair_type_buttons = []
    for hair_type, details in hair_types[lang].items():
        hair_type_buttons.append([
            InlineKeyboardButton(
                text=details['display'],
                callback_data=f"hair_type_{hair_type}"
            )
        ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=hair_type_buttons)
    
    # Xabarni yangilash
    await callback_query.message.edit_text(
        texts[lang]['select_hair_type'],
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith('hair_type_'))
async def hair_type_selected(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = user_data[user_id]["language"]
    hair_type = callback_query.data.split('_')[2]
    selected_hair_type[user_id] = hair_type
    
    # Sanalarni generatsiya qilish
    dates = generate_dates(lang)
    date_buttons = []
    
    # Har bir sana uchun tugma yaratish (2 ta ustun)
    row = []
    for display_date, callback_date in dates:
        row.append(InlineKeyboardButton(
            text=display_date,
            callback_data=callback_date
        ))
        
        if len(row) == 2:  # 2 ta ustun
            date_buttons.append(row)
            row = []
    
    if row:  # Agar oxirgi qator to'liq bo'lmasa
        date_buttons.append(row)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=date_buttons)
    await callback_query.message.edit_text(
        texts[lang]['select_date'],
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: any(c.data.startswith(f"{i}-2024") for i in range(1, 32)))
async def date_selected(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = user_data[user_id]["language"]
    
    selected_date[user_id] = callback_query.data.split('-', 1)[1]
    cosmetologist = selected_cosmetologist[user_id]
    duration = hair_types[lang][selected_hair_type[user_id]]["duration"]
    
    # Bo'sh vaqtlarni olish
    available_slots = get_available_slots(cosmetologist, selected_date[user_id], duration)
    
    # Vaqt tugmalarini yaratish (bir ustunda)
    time_buttons = []
    for start_time, end_time in available_slots:
        button_text = f"{start_time} - {end_time}"
        callback_data = f"time_{start_time}"
        time_buttons.append([
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=time_buttons)
    await callback_query.message.edit_text(
        f"{texts[lang]['select_time']}\n"
        f"⏱ {hair_types[lang][selected_hair_type[user_id]]['display']} - "
        f"{hair_types[lang][selected_hair_type[user_id]]['duration']} ",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith('time_'))
async def time_selected(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = user_data[user_id]["language"]
    
    # Tanlangan vaqtni saqlash
    selected_time[user_id] = callback_query.data.split('_')[1]
    
    # Tasdiqlash uchun ma'lumotlarni ko'rsatish
    cosmetologist = COSMETOLOGISTS_SCHEDULE[selected_cosmetologist[user_id]]["name"]
    hair_type = hair_types[lang][selected_hair_type[user_id]]["display"]
    date = selected_date[user_id]
    time = selected_time[user_id]
    duration = hair_types[lang][selected_hair_type[user_id]]["duration"]
    end_time = minutes_to_time(time_to_minutes(time) + duration)
    
    confirmation_text = (
        f"🔍 Quyidagi ma'lumotlarni tasdiqlaysizmi?\n\n"
        f"👤 Mijoz: {user_data[user_id]['name']}\n"
        f"📞 Telefon: {user_data[user_id]['phone']}\n"
        f"💅 Kosmetolog: {cosmetologist}\n"
        f"💇‍♀️ Xizmat: {hair_type}\n"
        f"📅 Sana: {date}\n"
        f"🕒 Vaqt: {time} - {end_time}\n"
        f"⏱ Davomiyligi: {duration} daqiqa"
    )
    
    if lang == 'ru':
        confirmation_text = (
            f"🔍 Подтверждаете следующие данные?\n\n"
            f"👤 Клиент: {user_data[user_id]['name']}\n"
            f"📞 Телефон: {user_data[user_id]['phone']}\n"
            f"💅 Косметолог: {cosmetologist}\n"
            f"💇‍♀️ Услуга: {hair_type}\n"
            f"📅 Дата: {date}\n"
            f"🕒 Время: {time} - {end_time}\n"
            f"⏱ Длительность: {duration} минут"
        )
    elif lang == 'en':
        confirmation_text = (
            f"🔍 Do you confirm the following details?\n\n"
            f"👤 Client: {user_data[user_id]['name']}\n"
            f"📞 Phone: {user_data[user_id]['phone']}\n"
            f"💅 Cosmetologist: {cosmetologist}\n"
            f"💇‍♀️ Service: {hair_type}\n"
            f"📅 Date: {date}\n"
            f"🕒 Time: {time} - {end_time}\n"
            f"⏱ Duration: {duration} minutes"
        )
    
    # Tasdiqlash tugmalari
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=texts[lang]['yes'], callback_data="confirm"),
            InlineKeyboardButton(text=texts[lang]['no'], callback_data="cancel")
        ]
    ])
    
    await callback_query.message.edit_text(
        confirmation_text,
        reply_markup=confirm_keyboard
    )

@dp.callback_query(lambda c: c.data == "confirm")
async def confirm_booking(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = user_data[user_id]["language"]
    
    # Buyurtmani saqlash
    cosmetologist = selected_cosmetologist[user_id]
    date = selected_date[user_id]
    start_time = selected_time[user_id]
    duration = hair_types[lang][selected_hair_type[user_id]]["duration"]
    end_time = minutes_to_time(time_to_minutes(start_time) + duration)
    
    # Band qilish
    if date not in COSMETOLOGISTS_SCHEDULE[cosmetologist]["appointments"]:
        COSMETOLOGISTS_SCHEDULE[cosmetologist]["appointments"][date] = []
    
    COSMETOLOGISTS_SCHEDULE[cosmetologist]["appointments"][date].append((start_time, end_time))
    
    # Tasdiqlash xabari
    success_message = texts[lang]['booking_confirmed'] + "\n\n"
    booking_details = (
        f"👤 {user_data[user_id]['name']}\n"
        f"📞 {user_data[user_id]['phone']}\n"
        f"💅 {COSMETOLOGISTS_SCHEDULE[cosmetologist]['name']}\n"
        f"💇‍♀️ {hair_types[lang][selected_hair_type[user_id]]['display']}\n"
        f"📅 {date}\n"
        f"🕒 {start_time} - {end_time}"
    )
    success_message += booking_details
    
    # Kanalga xabar yuborish
    channel_message = (
        f"🆕 YANGI BUYURTMA!\n\n"
        f"{booking_details}\n\n"
        f"✅ Tasdiqlandi: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    
    try:
        # Kanalga xabar yuborish
        await callback_query.bot.send_message(
            chat_id=CHANNEL_ID,
            text=channel_message,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Kanalga yuborishda xatolik: {e}")
        # Admin yoki dasturchiga xatolik haqida xabar yuborish mumkin
    
    # Yangi buyurtma tugmasi
    new_booking_keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text=texts[lang]['new_booking'],
            callback_data="start_new_booking"
        )
    ]])

    # Foydalanuvchiga tasdiqlash xabarini yuborish
    await callback_query.message.edit_text(
        success_message,
        reply_markup=new_booking_keyboard
    )

@dp.callback_query(lambda c: c.data == "cancel")
async def cancel_booking(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = user_data[user_id]["language"]
    
    await callback_query.message.edit_text(
        texts[lang]['booking_cancelled'],
        reply_markup=None
    )

@dp.callback_query(lambda c: c.data == "restart")
async def restart(callback_query: types.CallbackQuery):
    await start_command(callback_query.message)

@dp.callback_query(lambda c: c.data.startswith("booked_"))
async def booked_time_selected(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = user_data[user_id]["language"]
    await callback_query.answer(texts[lang]['time_booked'], show_alert=True)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    help_text = (
        f"Murojaat uchun:\n\n"
        f"👤 {message.from_user.full_name}\n"
        f"📞 {message.from_user.username or 'Username mavjud emas'}\n"
        f"💭 {message.text[6:] if len(message.text) > 6 else 'Xabar mavjud emas'}"
    )
    
    try:
        await bot.send_message(chat_id=channel_id, text=help_text)
        await message.answer("Sizning murojaatingiz qabul qilindi! Tez orada javob beramiz.")
    except Exception as e:
        await message.answer("Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")

# Kanalga xabar yuborish uchun tekshirish funksiyasi
async def check_channel_access():
    try:
        # Botning kanalda admin ekanligini tekshirish
        bot_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=bot.id)
        if bot_member.status not in ['administrator', 'creator']:
            print("OGOHLANTIRISH: Bot kanalda admin emas!")
            return False
        return True
    except Exception as e:
        print(f"Kanalga ulanishda xatolik: {e}")
        return False

# Bot ishga tushganda kanalga ulanishni tekshirish
@dp.startup()
async def on_startup():
    if not await check_channel_access():
        print("XATO: Bot kanalga ulana olmadi yoki kanalda admin huquqlari yo'q!")

# Yangi buyurtma uchun yangi handler
@dp.callback_query(lambda c: c.data == "start_new_booking")
async def start_new_booking(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = user_data[user_id]["language"]
    
    # Foydalanuvchi ma'lumotlarini saqlash
    user_data[user_id] = {
        "language": lang,
        "step": "name",
        "name": user_data[user_id].get("name"),
        "phone": user_data[user_id].get("phone")
    }
    
    # Kosmetologlarni ko'rsatish
    cosmetologist_buttons = []
    row = []
    for cosmetologist_id, cosmetologist in enumerate(COSMETOLOGISTS_SCHEDULE.items()):
        name = cosmetologist[1]["name"]
        button = InlineKeyboardButton(
            text=name,
            callback_data=f"cosmetologist_{cosmetologist[0]}"
        )
        row.append(button)
        if len(row) == 2 or cosmetologist_id == len(COSMETOLOGISTS_SCHEDULE) - 1:
            cosmetologist_buttons.append(row)
            row = []
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=cosmetologist_buttons)
    
    try:
        await callback_query.message.edit_text(
            texts[lang]['select_cosmetologist'],
            reply_markup=keyboard
        )
    except Exception as e:
        # Agar xatolik bo'lsa, yangi xabar yuboramiz
        await callback_query.message.answer(
            texts[lang]['select_cosmetologist'],
            reply_markup=keyboard
        )

async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Error: {str(e)}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
