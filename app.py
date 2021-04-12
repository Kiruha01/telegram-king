import os

from flask import Flask, request
import git
import telebot

from logic import database, db_setup
from logic.db_setup import State, User, Player
from logic.table import create_total_table, create_round_table

bot = telebot.TeleBot(os.environ.get("TELE_TOKEN"), threaded=False)


def state_of_user_is(state: State):
    def function(message) -> bool:
        user = database.get_user(message.chat.id)
        if user:
            return user.state == state.value
        else:
            return False

    return function


def sum_of_point(user: User):
    summ = 0
    for i in State:
        if 2 <= i.value <= 15:
            summ += getattr(user, i.name)
    return summ


def set_points_for_round(user, players, chat_id, count_of_cards, state, name_of_next_round, is_bribes=False):
    dictonary = database.points_for_3 if user.count_of_players == 3 else database.points_for_4
    if user.current_asking_player < user.count_of_players:
        setattr(players[user.current_asking_player - 1], state.name, count_of_cards * dictonary[state.name])

        user.current_asking_player += 1
        bot.send_message(chat_id, f"Сколько {'взяток' if is_bribes else 'карт'} взял "
                                  f"*{players[user.current_asking_player - 1].name}*?", parse_mode='markdown')
    elif user.current_asking_player == user.count_of_players:
        setattr(players[user.current_asking_player - 1], state.name, count_of_cards * dictonary[state.name])

        endl = "\n"
        bot.send_message(chat_id,
                         # f"Результаты - {endl.join([i.name + ' ' + str(sum_of_point(i)) for i in players])}")
                         "*Результаты*\n" + create_round_table(players, state.name), parse_mode='markdown')
        markup = telebot.types.InlineKeyboardMarkup()

        markup.add(telebot.types.InlineKeyboardButton(text='Раунд закончен', callback_data=State(state.value + 1).name))
        bot.send_message(chat_id, name_of_next_round, reply_markup=markup)
        user.current_asking_player += 1
    database.commit()


def set_points_for_negative_patchwork(user, player: Player, chat_id, text):
    points = text.split()
    if len(points) == db_setup.NUM_OF_ROUNDS:
        dictionary = database.points_for_3 if user.current_asking_player == 3 else database.points_for_4
        bribes = int(points[0]) * dictionary['negative_bribes']
        hearts = int(points[1]) * dictionary['negative_hearts']
        boys = int(points[2]) * dictionary['negative_boys']
        girls = int(points[3]) * dictionary['negative_girls']
        king = int(points[4]) * dictionary['negative_king']
        last = int(points[5]) * dictionary['negative_last']
        player.negative_patchwork = bribes + hearts + boys + girls + king + last
        user.current_asking_player += 1
        database.commit()
    else:
        bot.send_message(chat_id, "Указаны не все раунды!\nОтправь количество взяток ещё раз.")


def set_points_for_positive_patchwork(user, player: Player, chat_id, text):
    points = text.split()
    if len(points) == db_setup.NUM_OF_ROUNDS:
        dictionary = database.points_for_3 if user.current_asking_player == 3 else database.points_for_4
        bribes = int(points[0]) * dictionary['positive_bribes']
        hearts = int(points[1]) * dictionary['positive_hearts']
        boys = int(points[2]) * dictionary['positive_boys']
        girls = int(points[3]) * dictionary['positive_girls']
        king = int(points[4]) * dictionary['positive_king']
        last = int(points[5]) * dictionary['positive_last']
        player.positive_patchwork = bribes + hearts + boys + girls + king + last
        user.current_asking_player += 1
        database.commit()
    else:
        bot.send_message(chat_id, "Указаны не все раунды!\nОтправь количество взяток ещё раз.")


@bot.message_handler(commands=['del_players'])
def register(message: telebot.types.Message):
    database.del_all_players()
    bot.send_message(message.chat.id, text="Done")


@bot.message_handler(commands=['to'])
def register(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    user.state = State.positive_patchwork.value
    database.commit()
    bot.send_message(message.chat.id, text="Сколько?")


@bot.message_handler(commands=['start'])
def register(message: telebot.types.Message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('3', '4')
    bot.send_message(message.chat.id, text="Сколько человек будет играть?", reply_markup=keyboard)
    user = database.get_user(message.chat.id)
    if user:
        user.state = State.start.value
        database.del_players_by_creator(user.telegram_id)
    else:
        user = User(telegram_id=message.chat.id,
                    state=State.start.value,
                    count_of_players=0,
                    current_asking_player=0)
        database.add(user)
    database.commit()


# ======================= CALLS ======================
@bot.callback_query_handler(func=lambda call: True)  # call.data == "negative_bribes")
def start_negative_bribes(call: telebot.types.CallbackQuery):
    bot.edit_message_reply_markup(message_id=call.message.id, reply_markup=None, chat_id=call.message.chat.id)
    user = database.get_user(call.message.chat.id)
    user.state = getattr(State, call.data).value
    user.current_asking_player = 1
    player = database.get_players(call.message.chat.id)[0]
    if user.state == State.negative_bribes.value or user.state == State.negative_last.value or \
            user.state == State.positive_bribes.value or user.state == State.positive_last.value:
        bot.send_message(call.message.chat.id, f"Сколько взяток взял *{player.name}*?", parse_mode='markdown')
    elif user.state == State.negative_patchwork.value or user.state == State.positive_patchwork.value:
        bot.send_message(call.message.chat.id, f"Сколько карт взял *{player.name}* по каждой из категорий?\n"
                                               f"Отправь по одному числу в каждой строке для следующих раундов"
                                               f"\n\n```\n"
                                               f"Всего взяток\n"
                                               f"Червовых карт\n"
                                               f"Мальчиков\n"
                                               f"Девочек\n"
                                               f"Кинг\n"
                                               f"2 последние взятки```", parse_mode='markdown')
    else:
        bot.send_message(call.message.chat.id, f"Сколько карт взял *{player.name}*?", parse_mode='markdown')
    database.commit()


# ====================== START ========================
@bot.message_handler(func=state_of_user_is(State.start), content_types=['text'])
def get_count_of_users(message: telebot.types.Message):
    if message.text == "3" or message.text == "4":
        user = database.get_user(message.chat.id)
        user.count_of_players = int(message.text)
        user.current_asking_player = 1
        user.set_state(State.names)
        database.commit()
        keyboard = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text="Введите имя для _первого_ игрока:", reply_markup=keyboard, parse_mode='markdown')
    else:
        bot.send_message(message.chat.id, text="Вы ввели что-то не то")
        register(message)


# =================================== NAMES ========================
@bot.message_handler(func=state_of_user_is(State.names), content_types=['text'])
def get_count_of_users(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    if user.current_asking_player <= user.count_of_players:
        player = Player(creator=message.chat.id,
                        name=message.text)
        database.add(player)

    if user.current_asking_player == user.count_of_players:
        players = database.get_players(message.chat.id)
        bot.send_message(message.chat.id, f"Сегодняшние игроки - _{', '.join([i.name for i in players])}_",
                         parse_mode='markdown')
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Раунд закончен', callback_data="negative_bribes"))
        bot.send_message(message.chat.id, "Раунд 1 - Не брать взяток", reply_markup=markup)
    else:
        if user.current_asking_player == 1:
            bot.send_message(message.chat.id, "Введите имя для _второго_ игрока:", parse_mode='markdown')
        elif user.current_asking_player == 2:
            bot.send_message(message.chat.id, "Введите имя для _третьего_ игрока:", parse_mode='markdown')
        elif user.current_asking_player == 3:
            bot.send_message(message.chat.id, "Введите имя для _четвёртого_ игрока:", parse_mode='markdown')
        user.current_asking_player += 1
    database.commit()


@bot.message_handler(func=state_of_user_is(State.negative_bribes), content_types=["text"])
def negative_bribes(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.negative_bribes, "Раунд 2 - Не "
                                                                                                       "брать черви",
                             is_bribes=True)
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.negative_hearts), content_types=["text"])
def negative_hearts(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.negative_hearts, "Раунд 3 - Не "
                                                                                                       "брать мальчиков")
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.negative_boys), content_types=["text"])
def negative_boys(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.negative_boys, "Раунд 4 - Не "
                                                                                                     "брать девочек")
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.negative_girls), content_types=["text"])
def negative_girls(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.negative_girls, "Раунд 5 - Не "
                                                                                                      "брать Кинга")
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.negative_king), content_types=["text"])
def negative_king(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.negative_king, "Раунд 6 - Не "
                                                                                                     "брать две последние взятки")
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.negative_last), content_types=["text"])
def negative_last(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.negative_last, "Раунд 7 - "
                                                                                                     "Отрицательный "
                                                                                                     "ералаш",
                             is_bribes=True)
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.negative_patchwork), content_types=["text"])
def negative_patchwork(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_negative_patchwork(user, players[user.current_asking_player - 1], message.chat.id, message.text)
        if user.current_asking_player == user.count_of_players + 1:
            user.current_asking_player += 1
            database.commit()
            bot.send_message(message.chat.id, "Переходим к положительным раундам!")
            markup = telebot.types.InlineKeyboardMarkup()

            markup.add(telebot.types.InlineKeyboardButton(text='Раунд закончен',
                                                          callback_data=State.positive_bribes.name))
            bot.send_message(message.chat.id, "Раунд 1 - Брать взятки", reply_markup=markup)

        else:
            bot.send_message(message.chat.id,
                             f"Сколько карт взял *{players[user.current_asking_player - 1].name}* по каждой из категорий?",
                             parse_mode='markdown')
    except ValueError:
        bot.send_message(message.chat.id, "Введи числа, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.positive_bribes), content_types=["text"])
def positive_bribes(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.positive_bribes, "Раунд 2 - "
                                                                                                       "Брать черви",
                             is_bribes=True)
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.positive_hearts), content_types=["text"])
def positive_hearts(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.positive_hearts, "Раунд 3 - "
                                                                                                       "Брать мальчиков")
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.positive_boys), content_types=["text"])
def positive_boys(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.positive_boys, "Раунд 4 - "
                                                                                                     "Брать девочек")
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.positive_girls), content_types=["text"])
def positive_girls(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.positive_girls, "Раунд 5 - "
                                                                                                      "Брать Кинга")
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.positive_king), content_types=["text"])
def positive_king(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.positive_king, "Раунд 6 - "
                                                                                                     "Брать две последние взятки")
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.positive_last), content_types=["text"])
def positive_last(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_round(user, players, message.chat.id, int(message.text), State.positive_last, "Раунд 7 - "
                                                                                                     "Положительный "
                                                                                                     "ералаш",
                             is_bribes=True)
    except ValueError:
        bot.send_message(message.chat.id, "Введи число, пожалуйста.")


@bot.message_handler(func=state_of_user_is(State.positive_patchwork), content_types=["text"])
def positive_patchwork(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    try:
        set_points_for_positive_patchwork(user, players[user.current_asking_player - 1], message.chat.id, message.text)
        if user.current_asking_player == user.count_of_players + 1:
            user.current_asking_player += 1
            database.commit()
            bot.send_message(message.chat.id, "Игра окончена!")
            bot.send_message(message.chat.id, create_total_table(players), parse_mode='markdown')
            database.del_players_by_creator(user.telegram_id)

        else:
            bot.send_message(message.chat.id,
                             f"Сколько карт взял *{players[user.current_asking_player - 1].name}* по каждой из категорий?",
                             parse_mode='markdown')
    except ValueError:
        bot.send_message(message.chat.id, "Введи числа, пожалуйста.")


if os.environ.get("DEPLOY"):
    app = Flask(__name__)


    @app.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return '', 200


    @app.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(
            url="https://kinggame.pythonanywhere.com/bot")
        return "?", 200


    @app.route('/update_server', methods=['POST'])
    def github_webhook():
        if request.method == 'POST':
            repo = git.Repo('telegram-king')
            origin = repo.remotes.origin
            origin.pull()
            print("GITHUB: Repo was updated successfully")
            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong event type', 400

else:
    bot.remove_webhook()
    bot.polling(none_stop=True)
