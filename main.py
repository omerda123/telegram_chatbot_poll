from pymongo import MongoClient

from survey import insert_questions
import logging
import telegram
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, ConversationHandler
import bot_settings

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    custom_keyboard = ["כן", "לא"],
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=""" 
                             היי, האם תרצה להשתתף בסקר קצר לקראת הבחירות?
                               ניתן לצאת באמצעות /cancel
                           """,
                             reply_markup=reply_markup)

    return AGE


def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Goodbye")


AGE, GENDER, CITY, PARTY = range(4)


def age(update: Update, context: CallbackContext):
    custom_keyboard = ["18-30", "30-40", "40-50", "50-60"],
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text="בן כמה אתה?",
                             reply_markup=reply_markup)
    return GENDER


def gender(update: Update, context: CallbackContext):
    custom_keyboard = ["זכר", "נקבה", "אחר"],
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text="מה המין שלך?",
                             reply_markup=reply_markup)
    return CITY


def city(update: Update, context: CallbackContext):
    text = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text="מהי עיר מגוריך?", reply_markup=ReplyKeyboardRemove())

    return PARTY


def party(update: Update, context: CallbackContext):
    custom_keyboard = ["ליכוד", "כחול לבן", "שס", "ימינה"],
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text="איזה מפלגה את\ה מתכוון לבחור?",
                             reply_markup=reply_markup)
    return ConversationHandler.END


conv_handler = ConversationHandler(

    entry_points=[CommandHandler('start', start)],

    states={
        AGE: [MessageHandler(Filters.text, age)],

        GENDER: [MessageHandler(Filters.text, gender)],

        CITY: [MessageHandler(Filters.text, city)],

        PARTY: [MessageHandler(Filters.text, party)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
dispatcher.add_handler(conv_handler)

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
