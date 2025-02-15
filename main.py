from telebot import TeleBot
from telebot import types
from telebot import custom_filters
import random
from io import StringIO

import config
import messages
import jokes
import my_filters

bot = TeleBot(config.BOT_TOKEN)
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.ForwardFilter())
bot.add_custom_filter(custom_filters.IsReplyFilter())
bot.add_custom_filter(my_filters.IsUserAdminOfBot())
bot.add_custom_filter(my_filters.ContainsWordFilter())


# bot.add_custom_filter(custom_filters.TextContainsFilter())


@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.START_MESSAGE,
    )


@bot.message_handler(commands=["help"])
def handle_command_help(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.HELP_MESSAGE,
    )


@bot.message_handler(commands=["joke"])
def handle_command_joke(message: types.Message):
    bot.send_message(
        message.chat.id,
        random.choice(jokes.KNOWN_JOKES),
    )


@bot.message_handler(commands=['dog_file'])
def send_dog_photo_from_disc(message: types.Message):
    photo_file = types.InputFile('pics/img.png')
    bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_file,
    )


@bot.message_handler(commands=['dog'])
def send_dog_pic_by_file_id(message: types.Message):
    photo_file = config.DOG_PIC_FILE_ID
    bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_file,
    )


@bot.message_handler(commands=['dog_doc'])
def send_dog_as_doc(message: types.Message):
    photo_file = types.InputFile('pics/img.png')
    bot.send_document(
        chat_id=message.chat.id,
        document=photo_file,
    )


@bot.message_handler(commands=['dogs'])
def send_dogs_photo(message: types.Message):
    bot.send_photo(
        chat_id=message.chat.id,
        photo=config.DOG_PIC_URL,
        reply_to_message_id=message.id,
    )


@bot.message_handler(commands=['dogs_doc'])
def send_dogs_photo_as_file(message: types.Message):
    bot.send_document(
        chat_id=message.chat.id,
        document=config.DOG_PIC_URL,
    )


@bot.message_handler(commands=['file'])
def send_text_file(message: types.Message):
    file_doc = types.InputFile('text.txt')
    bot.send_document(
        chat_id=message.chat.id,
        document=file_doc,
    )


@bot.message_handler(commands=['text'], is_forwarded=True)
def handle_forwarded_text_command(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.dont_forward_commands,
    )


@bot.message_handler(commands=['text'])
def send_text_doc_from_memory(message: types.Message):
    file = StringIO()
    file.write('Hello!!!!!!!!!!!!\n')
    file.write('Your random number: ')
    file.write(str(random.randint(1, 100)))
    file.seek(0)
    file_text_doc = types.InputFile(file)
    bot.send_document(
        chat_id=message.chat.id,
        document=file_text_doc,
        visible_file_name='your-random-number.txt',
    )


@bot.message_handler(commands=['chat_id'])
def handle_chat_id_request(message: types.Message):
    text = f'Айди чата {message.chat.id}'
    bot.send_message(
        message.chat.id,
        text=text,
    )


@bot.message_handler(commands=['secret'], is_bot_admin=True)
def handle_admin_secret(message: types.Message):
    bot.send_message(
        message.chat.id,
        text=messages.secret_massage_for_admin,
    )


@bot.message_handler(commands=['secret'], is_bot_admin=False)
def handle_not_admin_request_secret(message: types.Message):
    bot.send_message(
        message.chat.id,
        text=messages.secret_massage_not_admin,
    )


@bot.message_handler(text=custom_filters.TextFilter(
    contains=['погода'],
    ignore_case=True,
))
def handle_weather_request(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Хорошая погода!',
    )


def is_cat_in_caption(message: types.Message):
    return message.caption and 'кот' in message.caption.lower()


@bot.message_handler(
    content_types=['photo'],
    contains_word='кот',
    # func=is_cat_in_caption
    )
def handle_photo_with_caption(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.great_cat,
        reply_to_message_id=message.id,
    )


@bot.message_handler(content_types=['photo'])
def handle_photo(message: types.Message):
    photo_file_id = message.photo[-1].file_id
    caption_text = 'Классное фото'
    if message.caption:
        caption_text += '\nПодпись: ' + message.caption
    bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_file_id,
        reply_to_message_id=message.id,
        caption=caption_text,
    )


@bot.message_handler(content_types=['sticker'])
def handle_sticer(message: types.Message):
    bot.send_sticker(
        chat_id=message.chat.id,
        sticker=message.sticker.file_id,
        reply_to_message_id=message.id,
    )


def is_hi_in_text(message: types.Message):
    return message.text and 'привет' in message.text.lower()


@bot.message_handler(func=is_hi_in_text)
def handle_hi_message_text(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='И тебе привет!',
    )


content_type_to_ru = {
    'text': 'текст',
    'photo': 'фото',
    'document': 'документ',
}


@bot.message_handler(is_reply=True)
def handle_reply_message(message: types.Message):
    message_type = message.reply_to_message.content_type
    if message_type in content_type_to_ru:
        message_type = content_type_to_ru[message_type]
    text = f'Вы ответили на это сообщение, тип {message_type}'
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_to_message_id=message.reply_to_message.id,
    )


@bot.message_handler(content_types=['text'])
def echo_message(message: types.Message):
    text = message.text
    if 'как дела' in text.lower():
        text = 'Хорошо! А у вас как?'
    elif ('пока' or 'до свидания') in text.lower():
        text = 'До новых встреч!'
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
    )


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
