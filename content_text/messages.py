from telegram_bot.utils import StatesUsers

# СООБЩЕНИЯ ОТ БОТА
stat_message = """Привет 👋

Ты попал в MAC_bot  тут много полезной информации)"""
start_admin_message = "Приветствую админ 👋"
not_command_message = "Такой команды нет"
not_in_group_message = "Для общения с этим ботом подпишись на канал!"
in_group_message = "Отлично!\n\n спасибо за подписку, давай начнём!"
sms_not_in_group_message = "Ты ещё не подписался на канал 🥺"
list_channel_message = "Список каналов:"
help_text_message = """Данный бот создан в целях помочь людям узнать о наших партнёрских каналах, в продвижении которых ты и можешь помочь, так же не забывай, что лично для тебя у нас есть партнёрская программа, где ты можешь получать баллы и за них покупать наш товар.

За доп.информацией и вопросами 👇"""
username_admin_message = "Для связ с админом\nпиши сюда 👇"
list_product_message = "Список товаров:"
application_part_message = """Подача заявки на партнёрскую программу:
1.Ваше полное имя:

2.Ваш возраст:

3.Почему хотите стать нашим партнёром?

4.Сколько вы хотите получать баллов?

5.На сколько долго вы собираетесь быть нашим партнёром"""
rules_message = """<i>Правила партнёрской программы:</i>
<b>Соглашаясь с нашими правилами, вы должны понимать, что мы ждём результат, не работа карается.</b>

1. Не проявление активности.
<b>Наказание:</b> Выговор

2.Накрутка, приглашение вторых акантов.
<b>Наказание:</b> Увольнение

3.Обман администрации.
<b>Наказание:</b> Увольнение

4.Проявление отклонений от работы
<b>Наказание:</b> Выговор

5.Попрошайничество к администратору
<b>Наказание:</b> Выговор

6.Покупка, продажа более 5 баллов за день.
<b>Наказание:</b> Увольнение"""
questionnaire_info_message = """Подача заявки на партнёрскую программу:
1.Ваше полное имя:

2.Ваш возраст:

3.Почему хотите стать нашим партнёром?

4.Сколько вы хотите получать баллов?

5.На сколько долго вы собираетесь быть нашим партнёром"""
list_strat_message = "👉🏻 Список стратегий"

add_admin_message = """ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""
not_admin_id_message = """Это не число, ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""
vip_c_message = """Условия у меня простые) 

‼️Тебе сейчас нужно будет создать новый аккаунт 1вин, перейдя по моей ссылке чтобы он был чистым - https://1wztiw.top/bets/home 
При регистрации тебе нужно ввести мой промокод: ZEV500 
Регистрировать аккаунт нужно по номеру телефона, так же можно через соц сети (если у тебя нет свободного номера телефона - можно использовать старый, могу подсказать как)‼️
После того, как создал акк, делаешь деп и велком

🎁Говорю честно - за твою активность я получу бонус!(в виде ваучеров, которые раздаю вам)
С тебя активность - с меня ViP, сигналы, Стратегии!
всё взаимно) 


Вступи в наши ряди VIP канала, где уже более 200+ человек!!!

После выполнение всех условий пиши менеджеру👇
"""

lite_message = """— Стратегия: Lite - 749₽ на 2-3 икс (75% проход) - при покупке объясняется:

как определить линию и в какую можно играть —"""
lite_pro_message = """— Стратегия: Lite_Pro - 1.499₽ на 2-4 и выше икс (85% и выше проход) - при покупке объясняется:
 
как определить линию и в какую можно играть, как определить когда будет сливная линия и в какие моменты не ставить —"""
mine_message = """— Дополнение: Mine - 500₽ на 1.40 и 1.80Х —"""
mine_pro_message = """— Дополнение: Mine_Pro - 750₽ на  1.80 и 2.50Х —

При покупке двух дополнений стоимость: 949₽ Выгодно!"""
lite_mine_message = "— Набор Lite: Стратегия Lite + Дополнение Mine - 1049₽ —"
lite_Pro_mine_Pro_message = "— Набор Lite_Pro: Стратегия Lite_Pro + дополнение Mine_Pro - 1.849₽ —"
strat_2_dop_2_message = """ —Набор Profit: 2 Стратегии, 2 дополнения - 3.000₽ —

(Так же вы можете собрать себе набор самостоятельно, но цена будет составляться без скидки)"""

obych_pro_message = "— Обучени PRO - 5.000₽  (Полное обучение)"
obych_lite_message = "— Обучение SMOl - 3.499₽  (Базовое обучение)"

strat_1_tovar_message = """Cтратегия "Lite"
 —О стратегии:
Вы сможете играть по ней на кэфы  от 2-3х (смотря от линии).
Гарантируем играть по ней от 2х.
—Стратегия:
-Мы ожидаем на линии момент от 5-9Х
-После мы ставим максимум 3 хода догоном на 2х.
Догон - играть на определённый кэф и увеличивать ставку если не зайдёт.
-Если мы забираем с первого или второго хода, тогда больше не ставим, если все три слило, тогда больше не ставим, ждём другого момента.
—Линия:
У нас есть два вида лини:
1.Положительная - когда чаще сего заходит и мало сливает.
2.Отрицательная - когда чаще всего сливает и часто крашет.
Краш - кэф от 1.01 - 1.09 Х
-В отрицательную линию играть нельзя!
-В положительную линию играть можно.
—Скрин:
Мы можем увидеть 2 момента.
6.63  — 2 хода слива и на третий взяли 2Х
5.71 — с первого хода забрали 2Х

Если, что-то не понятно или есть выпросы, писать 👇"""

strat_2_tovar_message = """Cтратегия "Lite_Pro"
 —О стратегии:
Вы сможете играть по ней на кэфы  от 2-4х (смотря от линии).
Гарантируем играть по ней от 2х.
—Стратегия:
-Мы ожидаем на линии момент от 10Х
-После мы ставим максимум 3 хода догоном на 2х.
Догон - играть на определённый кэф и увеличивать ставку если не зайдёт.
-Если мы забираем с первого или второго хода, тогда больше не ставим, если все три слило, тогда больше не ставим, ждём другого момента.
—Линия:
У нас есть два вида лини:
1.Положительная - когда чаще сего заходит и мало сливает.
2.Отрицательная - когда чаще всего сливает и часто крашет.
Краш - кэф от 1.01 - 1.09 Х
-В отрицательную линию играть нельзя!
-В положительную линию играть можно.
—Cкрин:
15.82  2 слива и на трейтий ход забираем 2х
Если, что-то не понятно или есть выпросы, писать 👇"""

strat_3_tovar_message = """Дополнение "Mine"
 —О стратегии:
Вы сможете играть по ней на кэфы  от 1.4 и 1.8х (смотря от линии).
—Дополнение:
-Мы ожидаем на линии момент от 5-9Х
-После мы ждём один слив и потом ставим 1.4 и 1.8
-Если мы забираем с первого тогда больше не ставим, если нет, то увеличиваем ставки и ставим сразу за ходом или же ждём другой момент.
—Линия:
У нас есть два вида лини:
1.Положительная - когда чаще сего заходит и мало сливает.
2.Отрицательная - когда чаще всего сливает и часто крашет.
Краш - кэф от 1.01 - 1.09 Х
-В отрицательную линию играть нельзя!
-В положительную линию играть можно.
—Скрин:
5.38, пропускаем ход, он сливает и ставим, 1.4 и 1.8 заходит.

Если, что-то не понятно или есть выпросы, писать 👇"""

strat_4_tovar_message = """Дополнение "Mine_PRO"
 —О стратегии:
Вы сможете играть по ней на кэфы  от 1.8 и 2.5х (смотря от линии).
—Дополнение:
-Мы ожидаем на линии момент от 10Х
-После мы ждём один слив и потом ставим 1.8 и 2.5
-Если мы забираем с первого тогда больше не ставим, если нет, то увеличиваем ставки и ставим сразу за ходом или же ждём другой момент.
—Линия:
У нас есть два вида лини:
1.Положительная - когда чаще сего заходит и мало сливает.
2.Отрицательная - когда чаще всего сливает и часто крашет.
Краш - кэф от 1.01 - 1.09 Х
-В отрицательную линию играть нельзя!
-В положительную линию играть можно.
—Скрин:
32.82, пропускаем ход, слив и ставим 1.8 и 2.5 - заходит

Если, что-то не понятно или есть выпросы, писать 👇"""

strat_5_tovar_message = f"{strat_1_tovar_message}\n\n\n{strat_3_tovar_message}"
strat_6_tovar_message = f"{strat_2_tovar_message}\n\n\n{strat_4_tovar_message}"
strat_7_tovar_message = f"{strat_1_tovar_message}\n\n\n{strat_2_tovar_message}\n\n\n{strat_3_tovar_message}\n\n\n{strat_4_tovar_message}"

MESSAGES = {
    "start": stat_message,
    "start_admin": start_admin_message,
    "not_command": not_command_message,
    "not_in_group": not_in_group_message,
    "in_group": in_group_message,
    "sms_not_in_group": sms_not_in_group_message,
    "list_channel": list_channel_message,
    "help_text": help_text_message,
    "username_admin": username_admin_message,
    "list_product": list_product_message,
    "application_part": application_part_message,
    "rules": rules_message,
    "questionnaire_info": questionnaire_info_message,
    "list_strat": list_strat_message,
    "add_admin": add_admin_message,
    "not_admin_id": not_admin_id_message,
    "vip_c": vip_c_message,

    "strat_1": lite_message,
    "strat_2": lite_pro_message,
    "strat_3": mine_message,
    "strat_4": mine_pro_message,
    "strat_5": lite_mine_message,
    "strat_6": lite_Pro_mine_Pro_message,
    "strat_7": strat_2_dop_2_message,

    "obych_lite": obych_pro_message,
    "obych_pro": obych_lite_message,

    "strat_1_tovar": strat_1_tovar_message,
    "strat_2_tovar": strat_2_tovar_message,
    "strat_3_tovar": strat_3_tovar_message,
    "strat_4_tovar": strat_4_tovar_message,
    "strat_5_tovar": strat_5_tovar_message,
    "strat_6_tovar": strat_6_tovar_message,
    "strat_7_tovar": strat_7_tovar_message,

}
