import io
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = '502653463:AAHho1YHYZ_3C5gZgqXuCvFbpOtT_xEDW6g'


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def ans_to_not_photo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='This is not a picture :(')


def ans_to_picture(bot, update):
    num_id = update.message.photo[-1].file_id
    photo = bot.getFile(num_id)
    with io.BytesIO() as image_buffer:
        photo.download(out=image_buffer)
        image_buffer.seek(0)
        #buf_faces = image_buffer
        #buf_smiles = image_buffer
        #buf_faces.seek(0)
        #buf_smiles.seek(0)
        bot.send_photo(chat_id=update.message.chat_id, photo=image_buffer)
        #bot.send_photo(chat_id=update.message.chat_id, photo=buf_faces)
        #bot.send_photo(chat_id=update.message.chat_id, photo=buf_smiles)


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    photo_handler = MessageHandler(Filters.photo, ans_to_picture)
    dispatcher.add_handler(photo_handler)

    not_photo_handler = MessageHandler((~Filters.photo), ans_to_not_photo, )
    dispatcher.add_handler(not_photo_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
