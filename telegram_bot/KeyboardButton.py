from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from cfg.config import URL_CHANNEL

# КНОПКИ МЕНЮ
btn_product = KeyboardButton("🛍 Cписок товаров 🛍")
btn_channel = KeyboardButton("📋 Список каналов 📋")
btn_part = KeyboardButton("👨‍👨‍👦‍👦 Партнёрская программа 👨‍👨‍👦‍👦")
btn_help = KeyboardButton("❔ Помощь ❔")
btn_admin = KeyboardButton("🤖 Администратор 🤖")

btn_sub_channel = InlineKeyboardButton(text="Подписаться", url=URL_CHANNEL)
btn_check_sub = InlineKeyboardButton(text="Проверить", callback_data="check")
btn_admin_url = InlineKeyboardButton(text="🤖 Админ 🤖", url="https://t.me/xX_715_Xx")

# СПИСОК ТОВАРОВ
btn_product_strat = InlineKeyboardButton(text="👉🏻 Cтратегии", callback_data="strat")
btn_product_obuch = InlineKeyboardButton(text="👉🏻 Обучения", callback_data="obuch")
btn_product_privat = InlineKeyboardButton(text="👉🏻 Вип-канал", callback_data="privat")

# 👉🏻 Cтратегии
btn_Lite = InlineKeyboardButton(text="Lite | 749₽ | 70бал", callback_data="strat_1")
btn_Lite_Pro = InlineKeyboardButton(text="Lite_Pro | 1499₽ | 140бал", callback_data="strat_2")
btn_Mine = InlineKeyboardButton(text="Mine | 500₽ ", callback_data="strat_3")
btn_Mine_Pro = InlineKeyboardButton(text="Mine_Pro | 750₽ |", callback_data="strat_4")
btn_Lite_Mine = InlineKeyboardButton(text="Lite + Mine | 1049₽ |", callback_data="strat_5")
btn_Lite_Pro_Mine_Pro = InlineKeyboardButton(text="Lite_Pro + Mine_Pro | 1849₽ |", callback_data="strat_6")
btn_start_dop = InlineKeyboardButton(text="2 Стратегии, 2 дополнения | 3000₽ |", callback_data="strat_7")

# 👉🏻 Обучения
btn_obych_Pro = InlineKeyboardButton(text="Обучени PRO | 5000₽ | (Полное обучение)", callback_data="obych_lite")
btn_obych_Lite = InlineKeyboardButton(text="Обучение SMOl | 3499₽ | (Базовое обучение)", callback_data="obych_pro")

# 👉🏻 ВИП КАНАЛ
btn_vip_c = InlineKeyboardButton(text="Пиши", url="https://t.me/HOOP_POV")
btn_pod = InlineKeyboardButton(text="Пиши", url="https://t.me/VovTred")

btn_back = InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="back")

# СПИСОК КАНАЛОВ
btn_channel_url_1 = InlineKeyboardButton(text="𝚆𝚈𝚉𝙰.𝙵𝚇 - 𝚂𝙸𝙶𝙽𝙰𝙻𝚂", url="https://t.me/WyzaFX")
btn_channel_url_2 = InlineKeyboardButton(text="⚡️ MAC SIGNAL ⚡️", url="https://t.me/MAC1win")
btn_channel_url_3 = InlineKeyboardButton(text="Global_mentor", url="https://t.me/global_mentor")

# ПРИНЯТЬ СОГЛАШЕНИЯ
btn_accept_sogl = InlineKeyboardButton(text="✅ Принимаю условия ✅", callback_data="accept_ysl")

btn_accept_user = InlineKeyboardButton(text="✅ ПРИНЯТЬ ПОЛЬЗОВАТЕЛЯ ✅", callback_data="accept_users")
btn_cancel_user = InlineKeyboardButton(text="❎ ОТКЛОНИТЬ ❎", callback_data="cancel_users")

# ПЕРЕВОД БАЛЛОВ
btn_transfer = InlineKeyboardButton(text="Перевести баллы", callback_data="trans")

# Кнопки админа
btn_ban = KeyboardButton("Дать бан")
btn_on_ban = KeyboardButton("Убрать бан")
btn_ball = KeyboardButton("Дать баллы")
btn_view_all_us = KeyboardButton("Вывод пользователей")
btn_view_all_ref = KeyboardButton("Вывод рефералов")
btn_add_admin = KeyboardButton("Добавить админа")

btn_cancel = KeyboardButton("Отмена")

BUTTON_TYPES = {
    "BTN_HOME": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_product, btn_channel).add(btn_part).add(btn_help, btn_admin),
    "BTN_HOME_ADMIN": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_ban, btn_on_ban).add(btn_view_all_us, btn_view_all_ref).add(btn_ball).add(btn_add_admin),

    "BTN_CANCEL": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel),
    "BTN_SUB": InlineKeyboardMarkup().add(btn_sub_channel).add(btn_check_sub),
    "ADMIN_URL": InlineKeyboardMarkup().add(btn_admin_url),

    "BTN_PRODUCT": InlineKeyboardMarkup().add(btn_product_strat).add(btn_product_obuch).add(btn_product_privat),
    "BTN_STRAT": InlineKeyboardMarkup().add(btn_Lite, btn_Lite_Pro).add(btn_Mine, btn_Mine_Pro).add(
        btn_Lite_Mine, btn_Lite_Pro_Mine_Pro).add(btn_start_dop).add(btn_back),
    "BTN_OBYCH": InlineKeyboardMarkup().add(btn_obych_Pro).add(btn_obych_Lite).add(btn_back),
    "BTN_VIP": InlineKeyboardMarkup().add(btn_vip_c).add(btn_back),
    "BTN_VIP_1": InlineKeyboardMarkup().add(btn_vip_c),
    "BTN_URL_CHAT": InlineKeyboardMarkup().add(btn_channel_url_1).add(btn_channel_url_2).add(btn_channel_url_3),
    "BTN_ACCEPT_SOGL": InlineKeyboardMarkup().add(btn_accept_sogl),
    "BTN_ACCEPT_USERS": InlineKeyboardMarkup().add(btn_accept_user).add(btn_cancel_user),
    "BTN_TRANSFER": InlineKeyboardMarkup().add(btn_transfer),
    "BTN_POD": InlineKeyboardMarkup().add(btn_pod),
}
