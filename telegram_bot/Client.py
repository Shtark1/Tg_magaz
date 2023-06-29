from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext, Dispatcher

from telegram_bot.utils import StatesUsers
from telegram_bot.KeyboardButton import BUTTON_TYPES
from content_text.messages import MESSAGES
from cfg.config import ADMIN_ID, ID_CHANNEL, BOT_NIK, BANNED_ID, TOKEN_YOOKASSA
from cfg.database import Database
from create_bot import dp, bot

from yoomoney import Quickpay, Client

db = Database('cfg/database')


# ===================================================
# =============== СТАНДАРТНЫЕ КОМАНДЫ ===============
# ===================================================
async def start_command(message: Message):
    if message.from_user.id in BANNED_ID:
            await message.answer(f"{message.from_user.full_name} пишите, что хотите, но вам выдан Бан за нарушение правил!")
    else:
        #   РЕФ СИСТЕМА
        if not db.user_exists(message.from_user.id):
            referer_id = str(message.text[7:])
            if referer_id != "":
                if referer_id != message.from_user.id:
                    db.add_user(message.from_user.id, message.from_user.username, referer_id)
                    try:
                        await bot.send_message(chat_id=referer_id, text="По вашей реферальной ссылке зарегестрировался новый пользователь!")
                    except:
                        pass
            else:
                db.add_user(message.from_user.id, message.from_user.username)

        user_channel_status = await bot.get_chat_member(chat_id=ID_CHANNEL, user_id=message.from_user.id)
        if user_channel_status["status"] != 'left':
            if message.from_user.id in ADMIN_ID:
                await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

            else:
                await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])

        else:
            await message.answer(MESSAGES['start'])
            await bot.send_message(message.from_user.id, MESSAGES["not_in_group"], reply_markup=BUTTON_TYPES["BTN_SUB"])
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(StatesUsers.all()[0])


# ===================================================
# =============== 🛍 Cписок товаров 🛍 ===============
# ===================================================
async def list_products(message: Message):
    if message.from_user.id in BANNED_ID:
        await message.answer(f"{message.from_user.full_name} пишите, что хотите, но вам выдан Бан за нарушение правил!")
    else:
        await message.answer(MESSAGES["list_product"], reply_markup=BUTTON_TYPES["BTN_PRODUCT"])


# =============== Cписок стратегий ===============
async def list_strat(callback: CallbackQuery):
    await callback.message.edit_text(MESSAGES["list_strat"], reply_markup=BUTTON_TYPES["BTN_STRAT"])


# =============== Покупка стратегий ===============
async def strat_buy(callback: CallbackQuery):
    all_mark = callback.message.reply_markup.inline_keyboard
    my_btn = None
    for marks in all_mark:
        for mark in marks:
            if callback.data == mark.callback_data:
                my_btn = mark

    number = my_btn.text.split("|")[1].strip("₽ ")

    id_pay = f"{callback.from_user.id}_{callback.message.message_id}"
    url_pay = str(payment(id_pay, number))

    state = dp.current_state(user=callback.from_user.id)
    await state.update_data(id_pay=id_pay)
    await state.update_data(url_pay=url_pay)

    print(callback.data)
    await state.update_data(tovar=callback.data)

    btn_pay_yoomoney = InlineKeyboardButton(text="Оплатить", url=url_pay)
    btn_check_pay = InlineKeyboardButton(text="Проверить оплату", callback_data="CHECK_PAY")
    btn_pay_cancel = InlineKeyboardButton(text="Отмена", callback_data="CANCEL")

    if db.count_referer(callback.from_user.id) >= 140 and my_btn.callback_data == "strat_2":
        btn_pay_ball = InlineKeyboardButton(text="Купить за баллы", callback_data="buy_ball_140")
        btn_pay1 = InlineKeyboardMarkup().add(btn_pay_yoomoney).add(btn_pay_ball).add(btn_check_pay).add(btn_pay_cancel)

    elif db.count_referer(callback.from_user.id) >= 70 and my_btn.callback_data == "strat_1":
        btn_pay_ball = InlineKeyboardButton(text="Купить за баллы", callback_data="buy_ball_70")
        btn_pay1 = InlineKeyboardMarkup().add(btn_pay_yoomoney).add(btn_pay_ball).add(btn_check_pay).add(btn_pay_cancel)
    else:
        btn_pay1 = InlineKeyboardMarkup().add(btn_pay_yoomoney).add(btn_check_pay).add(btn_pay_cancel)

    await callback.message.delete()
    await callback.message.answer(MESSAGES[f"{my_btn.callback_data}"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
    await callback.message.answer(f"💳 Ваш счёт на оплату {number}руб:", reply_markup=btn_pay1)
    await state.set_state(StatesUsers.all()[4])


# ФОРМИРОВАНИЕ ССЫЛКИ ДЛЯ ОПЛАТЫ
def payment(id_pay, value_yookassa):
    quickpay = Quickpay(
            receiver="4100116335995110",
            quickpay_form="shop",
            targets='Покупка',
            paymentType="SB",
            sum=value_yookassa,
            label=id_pay
            )

    return quickpay.base_url


# =============== 💵 ПРОВЕРКА ОПЛАТЫ 💵 =================
async def check_pay(callback: CallbackQuery, state: FSMContext):
    if callback.data == "CHECK_PAY":
        client = Client(TOKEN_YOOKASSA)
        id_pay = await state.get_data()
        history = client.operation_history(label=id_pay["id_pay"])

        btn_pay_url = InlineKeyboardButton(text="Оплатить", url=id_pay["url_pay"])
        btn_check_pay = InlineKeyboardButton(text="Проверить ещё раз", callback_data="CHECK_PAY")
        btn_pay_cancel = InlineKeyboardButton(text="Отмена", callback_data="CANCEL")
        btn_pay_again = InlineKeyboardMarkup().add(btn_pay_url).add(btn_check_pay).add(btn_pay_cancel)

        if not history.operations:
            await callback.message.edit_reply_markup()
            await callback.message.answer("Оплата не прошла!!!", reply_markup=btn_pay_again)
            await state.set_state(StatesUsers.all()[4])
        else:
            await callback.message.edit_reply_markup()
            all_data = await state.get_data()
            if callback.data in ["strat_1", "strat_2", "strat_3", "strat_4"]:
                with open(f'img/{callback.data}.jpg', 'rb') as photo:
                    await bot.send_photo(callback.from_user.id,photo=photo, caption=MESSAGES[f"{all_data['tovar']}_tovar"], reply_markup=BUTTON_TYPES["BTN_HOME"])
            elif callback.data == "strat_5":
                with open("img/strat_1.jpg", 'rb') as photo:
                    await bot.send_photo(callback.from_user.id, photo=photo, caption=MESSAGES["strat_1_tovar"], reply_markup=BUTTON_TYPES["BTN_VIP_1"])
                with open("img/strat_3.jpg", 'rb') as photo:
                    await bot.send_photo(callback.from_user.id, photo=photo, caption=MESSAGES["strat_3_tovar"], reply_markup=BUTTON_TYPES["BTN_VIP_1"])
            elif callback.data == "strat_6":
                with open("img/strat_2.jpg", 'rb') as photo:
                    await bot.send_photo(callback.from_user.id, photo=photo, caption=MESSAGES["strat_2_tovar"], reply_markup=BUTTON_TYPES["BTN_VIP_1"])
                with open("img/strat_4.jpg", 'rb') as photo:
                    await bot.send_photo(callback.from_user.id, photo=photo, caption=MESSAGES["strat_4_tovar"], reply_markup=BUTTON_TYPES["BTN_VIP_1"])
            elif callback.data == "strat_7":
                with open("img/strat_1.jpg", 'rb') as photo:
                    await bot.send_photo(callback.from_user.id, photo=photo, caption=MESSAGES["strat_1_tovar"], reply_markup=BUTTON_TYPES["BTN_VIP_1"])
                with open("img/strat_2.jpg", 'rb') as photo:
                    await bot.send_photo(callback.from_user.id, photo=photo, caption=MESSAGES["strat_2_tovar"], reply_markup=BUTTON_TYPES["BTN_VIP_1"])
                with open("img/strat_3.jpg", 'rb') as photo:
                    await bot.send_photo(callback.from_user.id, photo=photo, caption=MESSAGES["strat_3_tovar"], reply_markup=BUTTON_TYPES["BTN_VIP_1"])
                with open("img/strat_4.jpg", 'rb') as photo:
                    await bot.send_photo(callback.from_user.id, photo=photo, caption=MESSAGES["strat_4_tovar"], reply_markup=BUTTON_TYPES["BTN_VIP_1"])
            elif callback.data == "obych_lite":
                await callback.message.answer(f"Вы купили обучение Lite\nОтпишите нашему админу\n\nВаши данные:\nid: {callback.from_user.id}\nusername: {callback.from_user.username}", reply_markup=BUTTON_TYPES["BTN_VIP_1"])

            elif callback.data == "obych_pro":
                await callback.message.answer(f"Вы купили обучение Pro\nОтпишите нашему админу\n\nВаши данные:\nid: {callback.from_user.id}\nusername: {callback.from_user.username}", reply_markup=BUTTON_TYPES["BTN_VIP_1"])

            await callback.message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])

            await state.finish()

    elif callback.data == "buy_ball_70" or callback.data == "buy_ball_70":
        db.delete_referer(callback.from_user.id, int(callback.data[9:]))
        await callback.message.edit_reply_markup()
        await bot.send_message(callback.from_user.id, "Баланс пополнен", reply_markup=BUTTON_TYPES["BTN_HOME"])
        await state.finish()

    elif callback.data == "CANCEL":
        await callback.message.edit_reply_markup()
        await callback.message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])
        await state.finish()


# ===================================================
# =============== ОТМЕНА ===============
# ===================================================
async def cansel_pay(message: Message, state: FSMContext):
    if message.from_user.id in ADMIN_ID:
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        await bot.send_message(message.from_user.id, MESSAGES["start"], reply_markup=BUTTON_TYPES["BTN_HOME"])
    await state.finish()


# =============== Cписок Обучений ===============
async def list_obych(callback: CallbackQuery):
    await callback.message.edit_text("👉🏻 Список обучений:", reply_markup=BUTTON_TYPES["BTN_OBYCH"])


# =============== ВИП КАНАЛ ===============
async def vip_channel(callback: CallbackQuery):
    await callback.message.edit_text(MESSAGES["vip_c"], reply_markup=BUTTON_TYPES["BTN_VIP"])


# =============== ВИП КАНАЛ ===============
async def back_list(callback: CallbackQuery):
    await callback.message.edit_text(MESSAGES["list_product"], reply_markup=BUTTON_TYPES["BTN_PRODUCT"])


# ====================================================
# =============== 📋 СПИСОК КАНАЛОВ 📋 ===============
# ====================================================
async def list_channel(message: Message):
    if message.from_user.id in BANNED_ID:
        await message.answer(f"{message.from_user.full_name} пишите, что хотите, но вам выдан Бан за нарушение правил!")
    else:
        await message.answer(MESSAGES["list_channel"], reply_markup=BUTTON_TYPES["BTN_URL_CHAT"])


# =============================================================
# =============== 👨‍👨‍👦‍👦 Партнёрская программа 👨‍👨‍👦‍👦 ===============
# =============================================================
async def part_prog(message: Message):
    if message.from_user.id in BANNED_ID:
            await message.answer(f"{message.from_user.full_name} пишите, что хотите, но вам выдан Бан за нарушение правил!")
    else:
        if db.get_application(message.from_user.id)[0] == 0:
            await message.answer(MESSAGES["rules"], reply_markup=BUTTON_TYPES["BTN_ACCEPT_SOGL"], parse_mode="HTML")
        else:
            if db.get_application(message.from_user.id)[1] is None:
                await message.answer("Вы уже подали заявку!\nОна на рассмотрениие!", reply_markup=BUTTON_TYPES["BTN_HOME"])
            else:
                try:
                    if db.count_referer(message.from_user.id) == 0:
                        await message.answer(
                            f"Твой ID: {message.from_user.id}\nТвоя реферальная ссылка: https://t.me/{BOT_NIK}?start={message.from_user.id}"
                            f"\nКол-во рефералов: {db.count_referer(message.from_user.id)}",
                            reply_markup=BUTTON_TYPES["BTN_HOME"])
                    else:
                        await message.answer(
                            f"Твой ID: {message.from_user.id}\nТвоя реферальная ссылка: https://t.me/{BOT_NIK}?start={message.from_user.id}"
                            f"\nКол-во рефералов: {db.count_referer(message.from_user.id)}",
                            reply_markup=BUTTON_TYPES["BTN_TRANSFER"])
                except:
                    pass


# =============== ЗАПОЛНЕНИЕ АНКЕТЫ ===============
async def questionnaire_input(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(MESSAGES["questionnaire_info"], reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
    state = dp.current_state(user=callback.from_user.id)
    await state.set_state(StatesUsers.all()[1])


# =============== ОТПРАВКА АНКЕТЫ ===============
async def send_questionnaire(message: Message):
    if message.from_user.id in BANNED_ID:
            await message.answer(f"{message.from_user.full_name} пишите, что хотите, но вам выдан Бан за нарушение правил!")
    else:
        state = dp.current_state(user=message.from_user.id)
        if message.text.lower() == "отмена":
            if message.from_user.id in ADMIN_ID:
                await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

            else:
                await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])

        else:
            for admin_id_tg in ADMIN_ID:
                await bot.send_message(chat_id=admin_id_tg, text=f"От кого: https://t.me/{message.from_user.username}"
                                                                 f"\nid: ({message.from_user.id})\n\nТекст анкеты:\n{message.text}",
                                       reply_markup=BUTTON_TYPES["BTN_ACCEPT_USERS"])

            await message.answer("Заявка подана на рассмотрение!", reply_markup=BUTTON_TYPES["BTN_HOME"])
            db.edit_application(message.from_user.id)

        await state.finish()


# =============== 👨‍👨‍👦‍👦 Перевод баллов 👨‍👨‍👦‍👦 ===============
async def transfer_bal(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Введи количество баллов для перевода:", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
    state = dp.current_state(user=callback.from_user.id)
    await state.set_state(StatesUsers.all()[2])


# =============== 👨‍👨‍👦‍👦 Ввод имени для перевода 👨‍👨‍👦‍👦 ===============
async def name_transfer(message: Message, state: FSMContext):
    try:
        if 0 < int(message.text) <= db.count_referer(message.from_user.id):
            await state.update_data(ball_trans=message.text)
            await message.answer('Введи usernsme пользователя без "@" для перевода:', reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesUsers.all()[3])

        else:
            await message.answer("На вашем счету нет столько баллов\nВведи количество баллов для перевода:", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesUsers.all()[2])

    except:
        if message.text.lower() == "отмена":
            if message.from_user.id in ADMIN_ID:
                await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

            else:
                await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])
            await state.finish()
        else:
            await message.answer("Это не похоже на число!\nВведи количество баллов для перевода:", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesUsers.all()[2])


# =============== 👨‍👨‍👦‍👦 Проверка имени 👨‍👨‍👦‍👦 ===============
async def check_name(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        if message.from_user.id in ADMIN_ID:
            await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

        else:
            await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])
        await state.finish()

    else:
        try:
            all_data = await state.get_data()
            id_trans = db.transfer_ball_user(message.from_user.id, int(all_data["ball_trans"]), message.text)
            await message.answer("Перевод прошёл успешно!", reply_markup=BUTTON_TYPES["BTN_HOME"])
            await bot.send_message(chat_id=id_trans, text=f"Вам отправили {all_data['ball_trans']}Б\nОт: https://t.me/{message.from_user.username}")
            await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])
            await state.finish()
        except:
            await message.answer("Перевод не прошёл", reply_markup=BUTTON_TYPES["BTN_HOME"])
            await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])
            await state.finish()


# ===========================================
# =============== ❔ Помощь ❔ ===============
# ===========================================
async def help_text(message: Message):
    if message.from_user.id in BANNED_ID:
        await message.answer(f"{message.from_user.full_name} пишите, что хотите, но вам выдан Бан за нарушение правил!")
    else:
        await message.answer(MESSAGES["help_text"], reply_markup=BUTTON_TYPES["BTN_POD"])


# ===================================================
# =============== 🤖 Администратор 🤖 ===============
# ===================================================
async def contact_admin(message: Message):
    if message.from_user.id in BANNED_ID:
            await message.answer(f"{message.from_user.full_name} пишите, что хотите, но вам выдан Бан за нарушение правил!")
    else:
        await message.answer(MESSAGES["username_admin"], reply_markup=BUTTON_TYPES["ADMIN_URL"])


# =================================================
# =============== ПРОВЕРКА ПОДПИСКИ ===============
# =================================================
async def check_sub(message: Message):
    state = dp.current_state(user=message.from_user.id)
    user_channel_status = await bot.get_chat_member(chat_id=ID_CHANNEL, user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        await message.answer(MESSAGES['in_group'], reply_markup=BUTTON_TYPES["BTN_HOME"])
        state = dp.current_state(user=message.from_user.id)
        await state.finish()

    else:
        await bot.send_message(message.from_user.id, MESSAGES["not_in_group"], reply_markup=BUTTON_TYPES["BTN_SUB"])
        await state.set_state(StatesUsers.all()[0])


async def check_sub_q(callback: CallbackQuery):
    user_channel_status = await bot.get_chat_member(chat_id=ID_CHANNEL, user_id=callback.from_user.id)
    if user_channel_status["status"] != 'left':
        await callback.message.delete()
        await callback.message.answer(MESSAGES['in_group'], reply_markup=BUTTON_TYPES["BTN_HOME"])
        state = dp.current_state(user=callback.from_user.id)
        await state.finish()

    else:
        await callback.answer(MESSAGES["sms_not_in_group"], show_alert=True)


# ===================================================
# =============== НЕИЗВЕСТНАЯ КОМАНДА ===============
# ===================================================
async def unknown_command(message: Message):
    if message.from_user.id in BANNED_ID:
            await message.answer(f"{message.from_user.full_name} пишите, что хотите, но вам выдан Бан за нарушение правил!")
    else:
        if message.from_user.id in ADMIN_ID:
            await message.answer(MESSAGES['not_command'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        else:
            await bot.send_message(message.from_user.id, MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")

    dp.register_message_handler(list_products, lambda message: message.text == '🛍 Cписок товаров 🛍')
    dp.register_callback_query_handler(list_strat, lambda callback: callback.data == "strat")
    dp.register_callback_query_handler(strat_buy, lambda callback: callback.data == "strat_1" or callback.data == "strat_2"
                                       or callback.data == "strat_3" or callback.data == "strat_4" or callback.data == "strat_5"
                                       or callback.data == "strat_6" or callback.data == "strat_7" or callback.data == "obych_lite"
                                       or callback.data == "obych_pro")
    dp.register_callback_query_handler(check_pay, state=StatesUsers.STATE_4)
    dp.register_message_handler(cansel_pay, lambda message: message.text == 'Отмена', state=StatesUsers.STATE_4)

    dp.register_callback_query_handler(list_obych, lambda callback: callback.data == "obuch")
    dp.register_callback_query_handler(vip_channel, lambda callback: callback.data == "privat")
    dp.register_callback_query_handler(back_list, lambda callback: callback.data == "back")

    dp.register_message_handler(list_channel, lambda message: message.text == '📋 Список каналов 📋')

    dp.register_message_handler(part_prog, lambda message: message.text == '👨‍👨‍👦‍👦 Партнёрская программа 👨‍👨‍👦‍👦')
    # Заявка для партнёрки
    dp.register_callback_query_handler(questionnaire_input, lambda callback: callback.data == "accept_ysl")
    dp.register_message_handler(send_questionnaire, content_types="text", state=StatesUsers.STATE_1)
    # Перевод баллов
    dp.register_callback_query_handler(transfer_bal, lambda callback: callback.data == "trans")
    dp.register_message_handler(name_transfer, content_types="text", state=StatesUsers.STATE_2)
    dp.register_message_handler(check_name, content_types="text", state=StatesUsers.STATE_3)

    dp.register_message_handler(help_text, lambda message: message.text == '❔ Помощь ❔')
    dp.register_message_handler(contact_admin, lambda message: message.text == '🤖 Администратор 🤖')
    dp.register_message_handler(check_sub, state=StatesUsers.STATE_0)
    dp.register_callback_query_handler(check_sub_q, lambda callback: callback.data == "check", state=StatesUsers.STATE_0)

    dp.register_message_handler(unknown_command, content_types=["text"])
