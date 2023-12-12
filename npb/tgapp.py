import os

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from npb import handlers

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

tg_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
tg_app.add_handler(CommandHandler("start", handlers.start_command))
tg_app.add_handler(CommandHandler("delcontext", handlers.delcontext_command))
tg_app.add_handler(
    MessageHandler((filters.PHOTO & filters.CAPTION), handlers.photo_with_caption)
)
tg_app.add_handler(MessageHandler(filters.LOCATION, handlers.location))
tg_app.add_handler(MessageHandler(filters.TEXT, handlers.chat_message))
