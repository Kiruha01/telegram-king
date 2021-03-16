import telebot
from telebot.types import Message

bot = telebot.TeleBot('1357569041:AAF0gjrD3_YiXHkODt2aDXQGZI0mSVt0lew')


@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Ты начал")
    elif message.text == "Привет":
        bot.send_message(message.from_user.id, "Тевирп!")


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)