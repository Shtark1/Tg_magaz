import os
import re
from openpyxl import Workbook
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext, Dispatcher

from telegram_bot.utils import StatesAdmin
from telegram_bot.KeyboardButton import BUTTON_TYPES
from content_text.messages import MESSAGES
from cfg.config import ADMIN_ID, BANNED_ID
from cfg.database import Database
from create_bot import dp, bot

db = Database('cfg/database')


# ===================================================
# ===================== АДМИНКА =====================
# ===================================================

# =============== ДОБАВИТЬ АДМИНА ===============
async def add_admin(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES["add_admin"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[1])
    else:
        await bot.send_message(message.from_user.id, MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== ВВОД ID АДМИНА ===============
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        new_users_id = int(message.text)
        ADMIN_ID.append(new_users_id)
        await message.answer("Добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[1])


# ========================================================
# ===================== ПРИЁМ ЗАЯВОК =====================
# ========================================================
async def transfer_bal(callback: CallbackQuery):
    try:
        text_sms = callback.message.text
        match = re.search(r'id:\s*\((\d+)\)', text_sms).group(1)
        if callback.data == "accept_users":
            await callback.message.answer("✅ Пользователь принят ✅", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            await callback.answer()
            db.accept_or_cancel_ref(match, "True")
            await bot.send_message(chat_id=match, text="Вас приняли в партнёрку!")

        elif callback.data == "cancel_users":
            await callback.message.answer("❎ Пользователю отказанно ❎", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            await callback.answer()
            db.accept_or_cancel_ref(match, None)
            await bot.send_message(chat_id=match, text="Вам отказанно в партнёрке!")
    except:
        await callback.message.answer("!ОШИБКА!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await callback.answer()


# ===============================================================
# ===================== ДАТЬ/УБРАТЬ БАН =========================
# ===============================================================
async def add_ban(message: Message):
    if message.from_user.id in ADMIN_ID:
        if message.text.lower() == "дать бан":
            await message.answer('Впиш id пользователя для бана:', reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        else:
            await message.answer('Впиш id пользователя для того, что бы снять бан:', reply_markup=BUTTON_TYPES["BTN_CANCEL"])

        state = dp.current_state(user=message.from_user.id)
        await state.update_data(what_d=message.text)
        await state.set_state(StatesAdmin.all()[2])
    else:
        await bot.send_message(message.from_user.id, MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


# ===================== ДАТЬ/УБРАТЬ БАН =========================
async def check_ban(message: Message, state: FSMContext):
    try:
        all_data = await state.get_data()

        if message.text.lower() == "отмена":
            await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            await state.finish()

        elif all_data["what_d"] == "Дать бан":
            BANNED_ID.append(int(message.text))
            await message.answer('Пользователю выдан бан', reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        else:
            try:
                BANNED_ID.remove(int(message.text))
                await message.answer('Пользователю убран бан', reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            except:
                await message.answer('Этот пользователь не в бане', reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

        await state.finish()
    except:
        await message.answer('id состоит только из цифр\nПопробуй ввести ещё раз:', reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[2])


# ===============================================================
# =============== ВЫВОД ПОЛЬЗОВАТЕЛЕЙ/РЕФЕРАЛОВ =================
# ===============================================================
async def views_users(message: Message):
    if message.from_user.id in ADMIN_ID:
        if message.text.lower() == "вывод пользователей":
            write_to_excel_all_users(db.get_all_data(), "все_пользователи.xlsx")
            with open("все_пользователи.xlsx", 'rb') as file:
                await bot.send_document(message.from_user.id, file)
            await message.answer(MESSAGES["start"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            os.remove("все_пользователи.xlsx")
        else:
            all_data = db.get_partners()
            write_to_excel_all_part(all_data, "все_рефералы.xlsx")
            with open("все_рефералы.xlsx", 'rb') as file:
                await bot.send_document(message.from_user.id, file)
            await message.answer(MESSAGES["start"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            os.remove("все_рефералы.xlsx")
    else:
        await bot.send_message(message.from_user.id, MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


def write_to_excel_all_users(data, filename):
    workbook = Workbook()
    sheet = workbook.active
    headers = ["id", "user_id", "username", "кто пригласил", "Бан", "Реферал?", "Подал заявку?"]
    sheet.append(headers)
    for row in data:
        sheet.append(row)
    workbook.save(filename)


def write_to_excel_all_part(data, filename):
    workbook = Workbook()
    sheet = workbook.active
    headers = ["id", "user_id", "username", "кто пригласил", "Бан", "Реферал?", "Подал заявку?", "кого пригласил (id/username)"]
    sheet.append(headers)
    for row in data:
        if len(row) == 1:
            for r in row:
                sheet.append(r)
        else:
            a = []
            for ro in row:
                for r in ro:
                    a.append(r)
            sheet.append(a)
    workbook.save(filename)


# ========================================================
# =============== ПОПЛНИТЬ БАЛАНС БАЛЛОВ =================
# ========================================================
async def up_bal(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer("Введи id пользователя для пополнения баллов:", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[3])

    else:
        await bot.send_message(message.from_user.id, MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== ЗАПРОС КОЛИЧЕСТВА БАЛЛОВ =================
async def how_many_bal(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        try:
            await state.update_data(id_user_bal=int(message.text))
            await message.answer("Введи сколько баллов добавить пользователю:", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesAdmin.all()[4])
        except:
            await message.answer("ID состоит только из чисел!\nВведи ещё раз id пользователя:", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesAdmin.all()[3])


# =============== ДОБАВЛЕНИЕ БАЛЛОВ =================
async def add_bal_user(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        try:
            all_data = await state.get_data()
            db.up_ball(all_data["id_user_bal"], int(message.text))
            await message.answer("Баллы добавлены!")
            await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            await state.finish()
        except Exception as ex:
            print(ex)
            await message.answer("Баллы можно вводить только ввиде числа!\nВведи ещё раз:", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesAdmin.all()[4])


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(add_admin, lambda message: message.text.lower() == 'добавить админа')
    dp.register_message_handler(id_admin, state=StatesAdmin.STATES_1)

    # ПРИНЯТЬ/ОТКАЗАТЬ ПОЛЬЗОВАТЕЛУ В РЕФ СИСТЕМЕ
    dp.register_callback_query_handler(transfer_bal, lambda callback: callback.data == "accept_users" or callback.data == "cancel_users")

    # ДАТЬ/УБРАТЬ БАН
    dp.register_message_handler(add_ban, lambda message: message.text.lower() == 'дать бан' or message.text.lower() == 'убрать бан')
    dp.register_message_handler(check_ban, state=StatesAdmin.STATES_2)

    # ВЫВОД ПОЛЬЗОВАТЕЛЕЙ/РЕФЕРАЛОВ
    dp.register_message_handler(views_users, lambda message: message.text.lower() == 'вывод пользователей' or message.text.lower() == 'вывод рефералов')

    # ДАТЬ БАЛЛЫ
    dp.register_message_handler(up_bal, lambda message: message.text.lower() == 'дать баллы')
    dp.register_message_handler(how_many_bal, state=StatesAdmin.STATES_3)
    dp.register_message_handler(add_bal_user, state=StatesAdmin.STATES_4)

