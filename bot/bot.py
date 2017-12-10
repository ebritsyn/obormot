import io
import logging
import sys
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, RegexHandler,
                          ConversationHandler)
from utils.image_processing import find_faces_n_get_labels


def start(bot, update):
    reply_keyboard = [['Predict', 'Help', 'Cancel']]
    update.message.reply_text(
        "Im a bot, please talk to me!",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ACTION


def cancel(bot, update):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def action(bot, update):
    msg = update.message.text
    if msg == 'Predict':
        update.message.reply_text("Send me a photo, please")
        return PHOTO


def ans_to_not_photo(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='This is not a picture :(')


def ans_to_picture(bot, update):
    num_id = update.message.photo[-1].file_id
    photo = bot.getFile(num_id)
    with io.BytesIO() as image_buffer:
        photo.download(out=image_buffer)
        num_faces, scores, msg_buf = find_faces_n_get_labels(image_buffer)
        if num_faces == 0:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Faces not found')
        else:
            msg_buf.seek(0)
            bot.send_photo(chat_id=update.message.chat_id, photo=msg_buf)


def main():

    token = sys.argv[1]
    updater = Updater(token=token)
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
     %(message)s', level=logging.INFO)
    global ACTION, PHOTO
    ACTION, PHOTO = range(2)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            ACTION: [RegexHandler('^(Predict|Help|Cancel)$', action)],

            PHOTO: [MessageHandler(Filters.photo, ans_to_picture)]
             #       CommandHandler('skip', skip_photo)],

           # LOCATION: [MessageHandler(Filters.location, location),
            #           CommandHandler('skip', skip_location)],

           # BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
