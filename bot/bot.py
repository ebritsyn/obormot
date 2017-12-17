import io
import logging
import os
import sys
from threading import Thread
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from utils.image_processing import Model
from utils.database import DbConnection


class Bot:  # pylint: disable=too-few-public-methods

    def __init__(self, token):
        self.token = token
        self.model = Model()
        self.data = DbConnection('data.db')

    @staticmethod
    def _start(bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text="I'm a bot, please talk to me!")

    @staticmethod
    def parse_user(upd):
        mess = upd.message
        username = mess.chat.username
        name1 = mess.chat.first_name
        name2 = mess.chat.last_name
        chat_id = int(mess.chat.id)
        return username, name1, name2, chat_id

    @staticmethod
    def parse_message(upd):
        mess = upd.message
        mess_id = mess.message_id
        text = mess.text
        chat_id = int(mess.chat.id)
        return mess_id, text, chat_id

    def _ans_to_not_photo(self, bot, update):
        username, name1, name2, chat_id = self.parse_user(update)
        mess_id, text, chat_id = self.parse_message(update)
        self.data.add_user(username, name1, name2, chat_id)
        self.data.add_message(mess_id, text, chat_id)
        bot.send_message(chat_id=update.message.chat_id,
                         text='This is not a picture :(')

    def _ans_to_picture(self, bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=telegram.ChatAction.UPLOAD_PHOTO)
        num_id = update.message.photo[-1].file_id
        photo = bot.getFile(num_id)
        with io.BytesIO() as image_buffer:
            photo.download(out=image_buffer)
            num_faces, msg_buf = self.model.predict_labels(image_buffer)
            if num_faces == 0:
                bot.send_message(
                    chat_id=update.message.chat_id, text='Faces not found')
            else:
                msg_buf.seek(0)
                bot.send_photo(chat_id=update.message.chat_id, photo=msg_buf)

    def start(self):
        self.data.start()
        updater = Updater(token=self.token)
        dispatcher = updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
        %(message)s', level=logging.INFO)

        def _stop_and_restart():
            """Gracefully stop the Updater and replace the current process \
            with a new one"""
            updater.stop()
            os.execl(sys.executable, sys.executable, *sys.argv)

        def restart(bot, update):  # pylint: disable=unused-argument
            update.message.reply_text('Bot is restarting...')
            Thread(target=_stop_and_restart).start()

        start_handler = CommandHandler('start', self._start)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(
            CommandHandler('r', restart, filters=Filters.user(
                username='@ebritsyn')))

        photo_handler = MessageHandler(Filters.photo, self._ans_to_picture)
        dispatcher.add_handler(photo_handler)

        not_photo_handler = MessageHandler(
            (~Filters.photo), self._ans_to_not_photo)
        dispatcher.add_handler(not_photo_handler)

        updater.start_polling()
        updater.idle()
