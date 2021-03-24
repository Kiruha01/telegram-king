import os

from flask import Flask, request
import git
import telebot

from logic import database
from logic.db_setup import State, User, Player


bot = telebot.TeleBot(os.environ.get("TELE_TOKEN"), threaded=False)


def state_of_user_is(state: State):
    def function(message) -> bool:
        user = database.get_user(message.from_user.id)
        if user:
            return user.state == state.value
        else:
            return False
    return function


@bot.message_handler(commands=['start'])
def register(message: telebot.types.Message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('3', '4')
    bot.send_message(message.from_user.id, text="Сколько человек будет играть?", reply_markup=keyboard)
    user = database.get_user(message.from_user.id)
    if user:
        user.state = State.start.value
    else:
        user = User(telegram_id=message.from_user.id,
                    state=State.start.value,
                    count_of_players=0,
                    current_asking_player=0)
    database.push(user)


@bot.message_handler(func=state_of_user_is(State.start), content_types=['text'])
def get_count_of_users(message: telebot.types.Message):
    if message.text == "3" or message.text == "4":
        user = database.get_user(message.from_user.id)
        user.count_of_players = int(message.text)
        user.current_asking_player = 1
        user.set_state(State.names)
        database.push(user)
        keyboard = telebot.types.ReplyKeyboardMarkup(selective=False)
        bot.send_message(message.from_user.id, text="Введите имя для первого игрока:", reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, text="Вы ввели что-то не то")
        register(message)


@bot.message_handler(func=state_of_user_is(State.names), content_types=['text'])
def get_count_of_users(message: telebot.types.Message):
    player = Player(creator=message.from_user.id,
                    name=message.text)
    database.push(player)

    user = database.get_user(message.from_user.id)
    if user.current_asking_player == user.count_of_players:
        user.current_asking_player = 0
        user.set_state(State.negative_bribes)
        # players = database.get_players(message.from_user.id)
        # bot.send_message(message.from_user.id, f"Сегоднящние игроки - {}")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Раунд закончен', callback_data=3))
        bot.send_message(message.from_user.id, "РАУНД 1 - Не брать взяток", reply_markup=markup)
    else:
        if user.current_asking_player == 1:
            bot.send_message(message.from_user.id, "Введите имя для второго игрока:")
        elif user.current_asking_player == 2:
            bot.send_message(message.from_user.id, "Введите имя для третьего игрока:")
        elif user.current_asking_player == 3:
            bot.send_message(message.from_user.id, "Введите имя для четвёртого игрока:")
        user.current_asking_player += 1
    database.push(user)


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

            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong event type', 400

else:
    bot.remove_webhook()
    bot.polling(none_stop=True)
