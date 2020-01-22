from pymongo import MongoClient

from survey import insert_questions
import logging
import telegram
from telegram import Update
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
    client = MongoClient()
    db = client.get_database("survey")
    questions_collection = db.get_collection("questions")
    first_question = questions_collection.find_one({"id": 0})

    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    custom_keyboard = first_question['answers'],
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text=first_question['question'] +
                             """ניתן לצאת באמצעות /cancel""",
                             reply_markup=reply_markup)


def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Goodbye")


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    if text == "כן":
        context.bot.send_message(chat_id=update.message.chat_id, text="מעולה! תודה רבה!")
        client = MongoClient()
        db = client.get_database("survey")
        questions_collection = db.get_collection("questions")
        questions = questions_collection.find({})
        while True:
            for question in questions:
                custom_keyboard = question['answers'],
                reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=question['question'],
                                         reply_markup=reply_markup)

    else:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="לא נורא, נתראה פעם הבאה")

    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )


dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)
insert_questions()

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
