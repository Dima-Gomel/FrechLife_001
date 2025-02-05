from telebot import TeleBot, types
import random
import config, messages, jokes

bot = TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.START_MESSAGE
    )


@bot.message_handler(commands=["help"])
def handle_command_help(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.HELP_MESSAGE
    )


@bot.message_handler(commands=["joke"])
def handle_command_joke(message: types.Message):
    bot.send_message(
        message.chat.id,
        random.choice(jokes.KNOWN_JOKES)
    )


@bot.message_handler()
def echo_message(message: types.Message):
    text = message.text
    if 'привет' in text.lower():
        text = 'И тебе привет!'
    elif 'как дела' in text.lower():
        text = 'Хорошо! А у вас как?'
    elif 'пока' or 'до свидания' in text.lower():
        text = 'До новых встреч!'
    bot.send_message(
    message.chat.id,
    text
    )


bot.infinity_polling(skip_pending=True)
