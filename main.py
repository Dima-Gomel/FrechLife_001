from telebot import TeleBot, types
import random

import config
import messages
import jokes

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


@bot.message_handler(commands=['dogs'])
def send_dogs_photo(message: types.Message):
    bot.send_photo(
        chat_id=message.chat.id,
        photo=config.DOG_PIC_URL
    )


def is_cat_in_caption(message: types.Message):
    return message.caption and 'кот' in message.caption.lower()


@bot.message_handler(content_types=['photo'], func=is_cat_in_caption)
def handle_photo_with_caption(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Какой классный кот!'
    )


@bot.message_handler(content_types=['photo'])
def handle_photo(message: types.Message):
    if message.caption:
        print('Подпись: ', message.caption)
    else:
        print('Отсутствует подпись: ', message.caption)
    photo_file_id = message.photo[-1].file_id
    bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_file_id,
        reply_to_message_id=message.id
    )


@bot.message_handler(content_types=['sticker'])
def handle_sticer(message: types.Message):
    bot.send_sticker(
        chat_id=message.chat.id,
        sticker=message.sticker.file_id,
        reply_to_message_id=message.id
    )


@bot.message_handler(content_types=['text'])
def echo_message(message: types.Message):
    text = message.text
    if 'привет' in text.lower():
        text = 'И тебе привет!'
    elif 'как дела' in text.lower():
        text = 'Хорошо! А у вас как?'
    elif ('пока' or 'до свидания') in text.lower():
        text = 'До новых встреч!'
    bot.send_message(
        chat_id=message.chat.id,
        text=text
    )


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
