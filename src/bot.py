#!/usr/bin/env python
# pylint: disable=unused-argument

'''
telegram *bot*
~~~~~~~~~~~~~~

This module executes the Telegram bot for pyphoy-te
'''

import logging
from datetime import datetime, timedelta
from os import environ

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import scraper

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CITY, CATEGORY, RESULT = range(3)

CM = scraper.load_categories_map('assets/categories.json')

rep_cities = scraper.get_cities()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """TODO"""

    cities = [[c] for c in rep_cities.keys()]
    reply_keyboard = cities
    await update.message.reply_text(
        "¡Hola! Soy pypcol_bot. Te puedo brindar información del pico y placa hoy en Colombia.\n\n"
        "Elige una ciudad:"
        ,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="¿Ciudad?"
        ),
    )

    return CITY


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """TODO"""
    city = update.message.text
    context.user_data['city'] = rep_cities[city]
    logger.info("Chosen city %s", city)
    categories_in_use_url = scraper.url_builder(scraper.PYPHOY_URL, rep_cities[city], '', '')
    logger.info(scraper.get_categories_in_use(CM, categories_in_use_url))
    reply_keyboard = [[CM[cat]['text']] for cat in CM if cat in scraper.get_categories_in_use(CM, categories_in_use_url)]
    
    await update.message.reply_text(
        "Elige una categoria de pico y placa: ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="¿Categoria?"
        ),
    )

    return CATEGORY


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """TODO"""
    choose_v_id_cm = {y['text']: x for x, y in CM.items()}
    category = update.message.text
    date = datetime.now() - timedelta(hours=5)
    context.user_data['category'] = choose_v_id_cm[category]
    context.user_data['date'] = date.date().__str__()
    data = context.user_data
    result = scraper.get_pyp_info(scraper.url_builder(scraper.PYPHOY_URL, data['city'], CM[data['category']]['path'], ""))
    data['info'] = result
    logger.info(data)
    
    await update.message.reply_photo(CM[data['category']]['image_url'],
        parse_mode='HTML',
        caption="{} {} en {}\n".format(CM[data['category']]['emoji'],CM[data['category']]['text'], data['city'][1:].capitalize().replace('-', ' ')) +
        "🚫 <b>Retricción: {}</b>\n".format(data['date']) +
        "        Tienen restricción placas terminadas en: {}\n".format(data['info']['plate_num']) +
        "        <b>Horario establecido: </b>\n" +
        "{}".format("\n".join(["        * " + v for v in data['info']['banned_times']])),
        reply_markup=ReplyKeyboardRemove()
    )
    del choose_v_id_cm

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """TODO"""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(environ.get("TG_BOT_TOKEN")).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CITY: [MessageHandler(filters.Regex("^({city_options})$".format(city_options='|'.join(list(rep_cities.keys())))), city)],
            CATEGORY: [MessageHandler(filters.Regex("^({category_options})$".format(category_options='|'.join([CM[cat]['text'] for cat in CM]))), category)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()