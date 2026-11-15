# main.py - NEXT RUSSIA | ROLE PLAY
# Установка: pip install pyTelegramBotAPI
# Запуск: python main.py
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice

TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН_ОТ_BOTFATHER"
ADMIN_ID = 123456789  # ВСТАВЬ СЮДА СВОЙ ID
SBER_CARD = "2202 1234 5678 9012"  # ТВОЯ КАРТА СБЕРБАНК
SBER_NAME = "ИВАН И."  # ИМЯ НА КАРТЕ

bot = telebot.TeleBot(TOKEN)

# ===== УРОВНИ АДМИНКИ КАК В BLACK RUSSIA =====
# price_stars - от 30 ⭐, price_rub - рублями
LEVELS = [
    {"id": "helper", "name": "Хелпер", "lvl": "1 LVL", "stars": 30, "rub": 69, "desc": "Кик, мут, помощь игрокам"},
    {"id": "admin1", "name": "Администратор", "lvl": "2 LVL", "stars": 70, "rub": 149, "desc": "Кик, мут, бан, тюрьма"},
    {"id": "admin2", "name": "Старший Администратор", "lvl": "3 LVL", "stars": 150, "rub": 299, "desc": "Бан, разбан, выдача скинов"},
    {"id": "admin3", "name": "Главный Администратор", "lvl": "4 LVL", "stars": 300, "rub": 599, "desc": "Всё + слежка, лидерки"},
    {"id": "owner", "name": "Основатель", "lvl": "5 LVL", "stars": 600, "rub": 1199, "desc": "Всё + выдача админок, экономика"},
]

BANKS = {
    "nickel": {"name": "NICKEL", "emoji": "🟣", "desc": "Игровой банк NEXT RUSSIA\nПроцент: 5% в день\nЛимит: 1.000.000 ₽"},
    "sber": {"name": "СберБанк", "emoji": "🟢", "desc": "Настоящий банк для доната\nОплата рублями на карту\nПодтверждение чеком"},
}

users = {}  # user_id -> {balance, level, bank}
pending_rub = {}  # user_id -> level_id

def get_user(uid):
    if uid not in users:
        users[uid] = {"balance": 0, "level": "Игрок", "bank": "Нет", "nick": "Игрок"}
    return users[uid]

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        InlineKeyboardButton("🛡 Купить админку", callback_data="buy_admin"),
    )
    kb.add(
        InlineKeyboardButton("📊 Уровни админки", callback_data="levels"),
        InlineKeyboardButton("🏦 Банки", callback_data="banks"),
    )
    kb.add(
        InlineKeyboardButton("🟣 NICKEL", callback_data="bank_nickel"),
        InlineKeyboardButton("🟢 СберБанк", callback_data="bank_sber"),
    )
    kb.add(
        InlineKeyboardButton("⭐ Донат звёздами", callback_data="buy_admin"),
        InlineKeyboardButton("💳 Донат рублями", callback_data="buy_admin"),
    )
    kb.add(InlineKeyboardButton("📜 Правила", callback_data="rules"))
    return kb

def banks_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🟣 NICKEL", callback_data="bank_nickel"),
        InlineKeyboardButton("🟢 СберБанк", callback_data="bank_sber"),
    )
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    return kb

@bot.message_handler(commands=['start'])
def start(m):
    u = get_user(m.from_user.id)
    u["nick"] = m.from_user.first_name
    bot.send_message(m.chat.id,
        f"🇷🇺 <b>NEXT RUSSIA | ROLE PLAY</b>\n\n"
        f"Добро пожаловать, <b>{m.from_user.first_name}</b>!\n\n"
        f"🚗 Автомобили и недвижимость\n"
        f"🏢 Бизнес и заработок\n"
        f"👮 Государственные организации\n"
        f"👨‍👩‍👧 Семьи и друзья\n"
        f"💼 Карьера и развитие\n\n"
        f"🔥 <b>Создай свою историю в мире NEXT RUSSIA!</b>\n\n"
        f"🛡 Админка от <b>30 ⭐</b>\n"
        f"💳 Оплата: Звёзды и Рубли\n"
        f"🏦 Банки: NICKEL и СберБанк",
        parse_mode="HTML", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda c: c.data == "back")
def back(c):
    bot.edit_message_text("🇷🇺 <b>NEXT RUSSIA</b>\n\nВыбери раздел:", c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=main_menu())
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data == "profile")
def profile(c):
    u = get_user(c.from_user.id)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🛡 Купить админку", callback_data="buy_admin"))
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    bot.edit_message_text(
        f"👤 <b>Профиль</b>\n\n"
        f"🪪 Ник: <b>{u['nick']}</b>\n"
        f"🛡 Уровень: <b>{u['level']}</b>\n"
        f"💰 Баланс: <b>{u['balance']} ₽</b>\n"
        f"🏦 Банк: <b>{u['bank']}</b>\n"
        f"🆔 ID: <code>{c.from_user.id}</code>",
        c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=kb)
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data == "rules")
def rules(c):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    bot.edit_message_text(
        "📜 <b>Правила NEXT RUSSIA</b>\n\n"
        "1. Не оскорблять игроков и админов\n"
        "2. Не использовать читы\n"
        "3. Не обманывать при сделках\n"
        "4. Админка не даёт право нарушать правила\n"
        "5. Возврат доната - только по решению основателя",
        c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=kb)
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data == "levels")
def levels(c):
    text = "📊 <b>УРОВНИ АДМИНКИ - КАК В BLACK RUSSIA</b>\n\n"
    kb = InlineKeyboardMarkup(row_width=1)
    for lvl in LEVELS:
        text += f"<b>{lvl['name']} - {lvl['lvl']}</b>\n{lvl['desc']}\n⭐ {lvl['stars']} звёзд / 💳 {lvl['rub']} ₽\n\n"
        kb.add(InlineKeyboardButton(f"🛡 {lvl['name']} - {lvl['stars']} ⭐ / {lvl['rub']} ₽", callback_data=f"level_{lvl['id']}"))
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    bot.edit_message_text(text, c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=kb)
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data == "buy_admin")
def buy_admin(c):
    kb = InlineKeyboardMarkup(row_width=1)
    for lvl in LEVELS:
        kb.add(InlineKeyboardButton(f"🛡 {lvl['name']} - {lvl['stars']} ⭐ / {lvl['rub']} ₽", callback_data=f"level_{lvl['id']}"))
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    bot.edit_message_text(
        "🛡 <b>КУПИТЬ АДМИНКУ</b>\n\n"
        "Выбери уровень. Цена от <b>30 ⭐</b>.\n"
        "Оплата двумя способами:\n"
        "⭐ - Звёздами, сразу автоматически\n"
        "💳 - Рублями, через СберБанк, по чеку",
        c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=kb)
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("level_"))
def level_detail(c):
    lid = c.data.replace("level_", "")
    lvl = next((x for x in LEVELS if x["id"] == lid), None)
    if not lvl:
        return
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(f"⭐ Купить за {lvl['stars']} ⭐", callback_data=f"pay_stars_{lid}"),
        InlineKeyboardButton(f"💳 Купить за {lvl['rub']} ₽", callback_data=f"pay_rub_{lid}"),
    )
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="buy_admin"))
    bot.edit_message_text(
        f"🛡 <b>{lvl['name']} - {lvl['lvl']}</b>\n\n"
        f"{lvl['desc']}\n\n"
        f"⭐ Цена звёздами: <b>{lvl['stars']} ⭐</b>\n"
        f"💳 Цена рублями: <b>{lvl['rub']} ₽</b>\n\n"
        f"Выбери способ оплаты:",
        c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=kb)
    bot.answer_callback_query(c.id)@bot.callback_query_handler(func=lambda c: c.data.startswith("pay_stars_"))
def pay_stars(c):
    lid = c.data.replace("pay_stars_", "")
    lvl = next((x for x in LEVELS if x["id"] == lid), None)
    if not lvl:
        return
    # Оплата звёздами - Telegram Stars, валюта XTR, автоматически
    bot.send_invoice(
        c.message.chat.id,
        title=f"NEXT RUSSIA - {lvl['name']}",
        description=f"Админка {lvl['name']} {lvl['lvl']} в NEXT RUSSIA. {lvl['desc']}",
        invoice_payload=f"admin_{lid}_{c.from_user.id}",
        provider_token="",  # Для звёзд токен не нужен
        currency="XTR",
        prices=[LabeledPrice(f"{lvl['name']}", lvl["stars"])],
    )
    bot.answer_callback_query(c.id, "Открываю оплату звёздами ⭐")

@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q):
    bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def success_pay(m):
    payload = m.successful_payment.invoice_payload
    # payload: admin_helper_123456
    try:
        lid = payload.split("_")[1]
    except:
        lid = "helper"
    lvl = next((x for x in LEVELS if x["id"] == lid), LEVELS[0])
    u = get_user(m.from_user.id)
    u["level"] = f"{lvl['name']} {lvl['lvl']}"
    bot.send_message(m.chat.id,
        f"✅ <b>ОПЛАЧЕНО {lvl['stars']} ⭐!</b>\n\n"
        f"🛡 Тебе выдана админка: <b>{lvl['name']} {lvl['lvl']}</b>\n"
        f"📋 {lvl['desc']}\n\n"
        f"Добро пожаловать в команду NEXT RUSSIA!",
        parse_mode="HTML", reply_markup=main_menu())
    # Уведомление тебе как владельцу
    try:
        bot.send_message(ADMIN_ID, f"💰 НОВАЯ ПОКУПКА!\n@{m.from_user.username} ({m.from_user.id})\nКупил: {lvl['name']} за {lvl['stars']} ⭐")
    except:
        pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("pay_rub_"))
def pay_rub(c):
    lid = c.data.replace("pay_rub_", "")
    lvl = next((x for x in LEVELS if x["id"] == lid), None)
    if not lvl:
        return
    pending_rub[c.from_user.id] = lid
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ Я оплатил, отправил чек", callback_data=f"sent_check_{lid}"))
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="buy_admin"))
    bot.edit_message_text(
        f"💳 <b>ОПЛАТА РУБЛЯМИ - СберБанк</b>\n\n"
        f"🛡 Товар: <b>{lvl['name']} {lvl['lvl']}</b>\n"
        f"💰 Сумма: <b>{lvl['rub']} ₽</b>\n\n"
        f"🏦 Переведи на карту СберБанк:\n"
        f"<code>{SBER_CARD}</code>\n"
        f"Получатель: <b>{SBER_NAME}</b>\n\n"
        f"1. Открой СберБанк Онлайн\n"
        f"2. Переведи {lvl['rub']} ₽\n"
        f"3. Сделай скрин чека\n"
        f"4. Нажми кнопку ниже и пришли чек сюда\n\n"
        f"Админка выдаётся после проверки чека.",
        c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=kb)
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("sent_check_"))
def sent_check(c):
    bot.send_message(c.message.chat.id, "🧾 Пришли сюда фото чека из СберБанка. Я передам его владельцу на проверку.")
    bot.answer_callback_query(c.id)

@bot.message_handler(content_types=['photo'])
def photo_check(m):
    if m.from_user.id not in pending_rub:
        bot.send_message(m.chat.id, "Пришли чек после того как выберешь админку и нажмёшь «Я оплатил».")
        return
    lid = pending_rub[m.from_user.id]
    lvl = next((x for x in LEVELS if x["id"] == lid), LEVELS[0])
    bot.send_message(m.chat.id, "✅ Чек отправлен на проверку! Жди, админ выдаст админку в течение 10-30 минут.")
    # Тебе приходит чек
    try:
        bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
        bot.send_message(ADMIN_ID,
            f"🧾 НОВЫЙ ЧЕК!\n"
            f"От: @{m.from_user.username} ({m.from_user.id})\n"
            f"Товар: {lvl['name']} за {lvl['rub']} ₽\n\n"
            f"Чтобы выдать админку, напиши:\n"
            f"<code>/give {m.from_user.id} {lid}</code>",
            parse_mode="HTML")
    except:
        pass

@bot.message_handler(commands=['give'])
def give_admin(m):
    if m.from_user.id != ADMIN_ID:
        bot.send_message(m.chat.id, "⛔ Только владелец.")
        return
    try:
        _, uid, lid = m.text.split()
        uid = int(uid)
        lvl = next((x for x in LEVELS if x["id"] == lid), None)
        if not lvl:
            bot.send_message(m.chat.id, "Нет такого уровня. helper / admin1 / admin2 / admin3 / owner")
            return
        u = get_user(uid)
        u["level"] = f"{lvl['name']} {lvl['lvl']}"
        if uid in pending_rub:
            del pending_rub[uid]
        bot.send_message(m.chat.id, f"✅ Выдал {lvl['name']} пользователю {uid}")
        bot.send_message(uid,
            f"✅ <b>ЧЕК ПОДТВЕРЖДЁН!</b>\n\n"
            f"🛡 Тебе выдана админка: <b>{lvl['name']} {lvl['lvl']}</b>\n"
            f"💳 Оплата рублями подтверждена.",
            parse_mode="HTML", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(m.chat.id, f"Используй так: /give 123456 helper\nОшибка: {e}")

@bot.callback_query_handler(func=lambda c: c.data == "banks")
def banks(c):
    kb = banks_menu()
    bot.edit_message_text(
        "🏦 <b>БАНКИ NEXT RUSSIA</b>\n\n"
        "🟣 <b>NICKEL</b> - игровой банк, проценты, вклады\n"
        "🟢 <b>СберБанк</b> - настоящий банк, донат рублями\n\n"
        "Выбери банк:",
        c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=kb)
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data == "bank_nickel")
def bank_nickel(c):
    u = get_user(c.from_user.id)
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("💰 Открыть вклад", callback_data="nickel_open"),
        InlineKeyboardButton("💸 Снять", callback_data="nickel_take"),
    )
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="banks"))
    bot.edit_message_text(
        "🟣 <b>NICKEL</b>\n\n"
        "Игровой банк NEXT RUSSIA\n"
        "Процент: <b>5% в день</b>\n"
        "Лимит: <b>1.000.000 ₽</b>\n"
        "Твой вклад: <b>0 ₽</b>\n\n"
        "Открой вклад и получай проценты каждый день.",
        c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=kb)
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data == "bank_sber")
def bank_sber(c):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🛡 Купить админку рублями", callback_data="buy_admin"))
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="banks"))
    bot.edit_message_text(
        "🟢 <b>СберБанк</b>\n\n"
        "Настоящий банк для доната.\n\n"
        f"Карта: <code>{SBER_CARD}</code>\n"
        f"Получатель: <b>{SBER_NAME}</b>\n\n"
        "Оплата админки рублями - переводишь на эту карту, присылаешь чек, получаешь админку.\n\n"
        "Цены от <b>69 ₽</b> за Хелпера.",
        c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=kb)
    bot.answer_callback_query(c.id)

@bot.callback_query_handler(func=lambda c: c.data in ["nickel_open", "nickel_take"])
def nickel_action(c):
    u = get_user(c.from_user.id)
    u["bank"] = "NICKEL"
    if c.data == "nickel_open":
        bot.answer_callback_query(c.id, "🟣 Вклад в NICKEL открыт!")
        bot.send_message(c.message.chat.id, "🟣 Вклад в NICKEL открыт! Завтра +5% к вкладу.")
    else:
        bot.answer_callback_query(c.id, "💸 Снял с NICKEL")
        bot.send_message(c.message.chat.id, "💸 Снял деньги с NICKEL.")

print("NEXT RUSSIA бот ожил! 🇷🇺")
bot.infinity_polling()
