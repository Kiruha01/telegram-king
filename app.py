import os

from flask import Flask, request
import git
import telebot

from logic import database

bot = telebot.TeleBot(os.environ.get("TELE_TOKEN"), threaded=False)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Ты начал")
    elif message.text == "Привет":
        bot.send_message(message.from_user.id, "Тевирп!")
    else:
        bot.send_message(message.from_user.id, "Хмм...")


if os.environ.get("DEPLOY"):
    app = Flask(__name__)


    @app.route("/bot/", methods=['POST'])
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
