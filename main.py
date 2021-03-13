#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import re
import urllib

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

wait = 1

def isValidURL(str):
 
    # Regex to check valid URL 
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
     
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty 
    # return false
    if (str == None):
        return False
 
    # Return if the string 
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False

# https://www.tiktok.com/?is_copy_url=1&is_from_webapp=v2&item_id=6926894548593413377#/@feruz__vines/video/6926894548593413377
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_html(
        'Hey!\nI can help you downloading videos from <b>You Tube</b>, <b>Tik Tok</b> and <b>Instagram</b>.\nJust send me the link :)'
    )
    return wait


def get_link(update, context):
    try:
        url = update.message.text
        if isValidURL(url):
            update.message.reply_text(update.message.text)
        else:
            update.message.reply_html('Mmmm.. Seems something wrong url that you sent :(\nplease check and retry...')
    except Exception as e:
        print('Error', str(e))


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("1671325575:AAF58GWYnXtint8QGbQzBRWjuUAdROJgoDY")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            wait: [MessageHandler(Filters.text, get_link)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
