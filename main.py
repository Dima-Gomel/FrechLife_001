from telebot import TeleBot, types
import random
import config

bot = TeleBot(config.BOT_TOKEN)

help_message = """Привет! Доступные команды:
- /start - начало работы с ботом
- /help - помощь (это сообщение)
- /joke - случайная шутка

Этот бот отправит вам тоже сообщение, что и вы ему.
"""

KNOWN_JOKES = [
    'В 47–ой книге Гарри Поттер убивает Джоан Роулинг.',
    'В пиве мало витаминов – вот почему его приходится пить так много.',
    'Новая секретарша английского не знала, но языком владела в совершенстве…'
]


@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(
        message.chat.id,
        'Привет! Давай знакомиться!'
    )


@bot.message_handler(commands=["help"])
def handle_command_help(message: types.Message):
    bot.send_message(
        message.chat.id,
        help_message
    )


@bot.message_handler(commands=["joke"])
def handle_command_joke(message: types.Message):
    bot.send_message(
        message.chat.id,
        random.choice(KNOWN_JOKES)
    )

@bot.message_handler()
def echo_message(message: types.Message):
    text = message.text
    if 'привет' in text.lower():
        text = 'Привет! Как дела?'
    bot.send_message(
    message.chat.id,
    text
    )


bot.infinity_polling(skip_pending=True)
