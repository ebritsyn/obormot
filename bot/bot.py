import io
import logging
import sys
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, RegexHandler,
                          ConversationHandler)
from utils.image_processing import find_faces_n_get_labels


def start(bot, update):
    reply_keyboard1 = [['Predict', 'Help', 'Cancel']]
    update.message.reply_text(
        "Im a bot, please talk to me!",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True))
    return CHOOSE_ACTION


def cancel(bot, update):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def choose_action(bot, update):
    msg = update.message.text
    if msg == "Predict":
        return PREDICT
    elif msg == "Help":
        return HELP_US
    elif msg == "Menu":
        reply_keyboard1 = [['Predict', 'Help', 'Cancel']]
        update.message.reply_text("Ok, What else?",
                                  reply_markup=ReplyKeyboardMarkup(
                                      reply_keyboard1,
                                      one_time_keyboard=True))
        return CHOOSE_ACTION


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
            reply_keyboard1 = [['Predict', 'Help', 'Cancel']]
            msg_buf.seek(0)
            bot.send_photo(chat_id=update.message.chat_id, photo=msg_buf)
            update.message.reply_text("Done!\nWhat else?",
                                      reply_markup=ReplyKeyboardMarkup(
                                          reply_keyboard1,
                                          one_time_keyboard=True))
            return CHOOSE_ACTION


def help_us(bot, update):
    update.message.reply_text("TO BE DONE!")
    reply_keyboard1 = [['Predict', 'Help', 'Cancel']]
    update.message.reply_text("What else?",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard1,
                                                               one_time_keyboard=True))
    return CHOOSE_ACTION


def predict(bot, update):
    reply_keyboard2 = [['Menu','Cancel']]
    update.message.reply_text("Send me a photo, please", reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
    return PHOTO


def main():

    token = sys.argv[1]
    updater = Updater(token=token)
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
     %(message)s', level=logging.INFO)
    global CHOOSE_ACTION, PHOTO, CANCEL, PREDICT, HELP_US
    CHOOSE_ACTION, PHOTO, CANCEL, PREDICT, HELP_US = range(5)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],#, RegexHandler('^(Predict)$', predict), RegexHandler('^(Help)$', help_us), RegexHandler('^(Cancel)$', cancel)],

        states={
            CHOOSE_ACTION: [RegexHandler('^(Predict)$', predict),
                            RegexHandler('^(Help)$', help_us)],

            PHOTO: [MessageHandler(Filters.photo, ans_to_picture),
                    RegexHandler('^(Menu)$', choose_action)],

            HELP_US: [RegexHandler('^(Help)$', help_us)],

            PREDICT: [RegexHandler('^(Predict)$', predict)]
        },

        fallbacks=[RegexHandler('^(Cancel)$', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
