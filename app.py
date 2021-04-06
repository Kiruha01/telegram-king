import os

from flask import Flask, request
import git
import telebot

from logic import database
from logic.db_setup import State, User, Player


bot = telebot.TeleBot(os.environ.get("TELE_TOKEN"), threaded=False)


def state_of_user_is(state: State):
    def function(message) -> bool:
        user = database.get_user(message.chat.id)
        if user:
            return user.state == state.value
        else:
            return False
    return function


@bot.message_handler(commands=['del_players'])
def register(message: telebot.types.Message):

    database.del_all_players()
    bot.send_message(message.chat.id, text="Done")


@bot.message_handler(commands=['start'])
def register(message: telebot.types.Message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('3', '4')
    bot.send_message(message.chat.id, text="Сколько человек будет играть?", reply_markup=keyboard)
    user = database.get_user(message.chat.id)
    if user:
        user.state = State.start.value
    else:
        user = User(telegram_id=message.chat.id,
                    state=State.start.value,
                    count_of_players=0,
                    current_asking_player=0)
        database.add(user)
    database.commit()


@bot.message_handler(func=state_of_user_is(State.start), content_types=['text'])
def get_count_of_users(message: telebot.types.Message):
    if message.text == "3" or message.text == "4":
        user = database.get_user(message.chat.id)
        user.count_of_players = int(message.text)
        user.current_asking_player = 1
        user.set_state(State.names)
        database.commit()
        keyboard = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text="Введите имя для первого игрока:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, text="Вы ввели что-то не то")
        register(message)


@bot.message_handler(func=state_of_user_is(State.names), content_types=['text'])
def get_count_of_users(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    if user.current_asking_player <= user.count_of_players:
        player = Player(creator=message.chat.id,
                        name=message.text)
        database.add(player)

    if user.current_asking_player == user.count_of_players:
        user.current_asking_player = 0
        user.set_state(State.negative_bribes)
        players = database.get_players(message.chat.id)
        bot.send_message(message.chat.id, f"Сегоднящние игроки - {', '.join([i.name for i in players])}")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Раунд закончен', callback_data="no_bribes"))
        bot.send_message(message.chat.id, "РАУНД 1 - Не брать взяток", reply_markup=markup)
    else:
        if user.current_asking_player == 1:
            bot.send_message(message.chat.id, "Введите имя для второго игрока:")
        elif user.current_asking_player == 2:
            bot.send_message(message.chat.id, "Введите имя для третьего игрока:")
        elif user.current_asking_player == 3:
            bot.send_message(message.chat.id, "Введите имя для четвёртого игрока:")
        user.current_asking_player += 1
    database.commit()


@bot.callback_query_handler(func=lambda call: call.data == "no_bribes")
def start_negative_bribes(call: telebot.types.CallbackQuery):
    bot.edit_message_reply_markup(message_id=call.message.id, reply_markup=None, chat_id=call.message.chat.id)
    print(call.message.chat.id)
    user = database.get_user(call.message.chat.id)
    user.state = State.negative_bribes.value
    user.current_asking_player = 1
    player = database.get_players(call.message.chat.id)[0]
    bot.send_message(call.message.chat.id, f"Сколько взяток взял {player.name}?")


@bot.message_handler(func=state_of_user_is(State.negative_bribes), content_types=["text"])
def negative_bribes(message: telebot.types.Message):
    user = database.get_user(message.chat.id)
    players = database.get_players(message.chat.id)
    if user.current_asking_player < user.count_of_players:
        try:
            ## TODO: Предусмотреть различгые варианты
            players[user.current_asking_player - 1].negative_bribes = int(message.text)
            user.current_asking_player += 1
            bot.send_message(message.chat.id, f"Сколько взяток взял {players[user.current_asking_player-1].name}?")
        except ValueError:
            bot.send_message(message.chat.id, "Введи число, пожалуйста.")
    elif user.current_asking_player == user.count_of_players:
        try:
            players[user.current_asking_player - 1].negative_bribes = int(message.text)
            bot.send_message(message.chat.id, f"Результаты - {', '.join([i.name + ' ' + str(i.negative_bribes) for i in players])}")
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Раунд закончен', callback_data="negative_hearts"))
            bot.send_message(message.chat.id, "РАУНД 2 - Не брать черви", reply_markup=markup)
            user.current_asking_player += 1
        except ValueError:
            bot.send_message(message.chat.id, "Введи число, пожалуйста.")
    database.commit()





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
