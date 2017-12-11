import io
import logging
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from utils.image_processing import find_faces_n_get_labels
from utils.database2 import DbConnection


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="I'm a bot, please talk to me!")


def ans_to_not_photo(bot, update):
    data = DbConnection('data.db')
    data.add_user(update)
    data.add_message(update)
    bot.send_message(chat_id=update.message.chat_id,
                     text='This is not a picture :(')


def ans_to_picture(bot, update):
    num_id = update.message.photo[-1].file_id
    photo = bot.getFile(num_id)
    with io.BytesIO() as image_buffer:
        photo.download(out=image_buffer)
        num_faces, msg_buf = find_faces_n_get_labels(image_buffer)
        if num_faces == 0:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Faces not found')
        else:
            msg_buf.seek(0)
            bot.send_photo(chat_id=update.message.chat_id, photo=msg_buf)


def main():

    token = sys.argv[1]
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
     %(message)s', level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    photo_handler = MessageHandler(Filters.photo, ans_to_picture)
    dispatcher.add_handler(photo_handler)

    not_photo_handler = MessageHandler((~Filters.photo), ans_to_not_photo, )
    dispatcher.add_handler(not_photo_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
