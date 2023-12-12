from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger

from npb.openai import (
    get_vision_response,
    get_location_completion,
    destroy_thread,
    send_thread_message,
)
from npb.utils import encode_photo_file_to_base64
from npb.s3 import read_thread_id


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("North Pole Buddy is ready, Ho ho ho")


async def delcontext_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    thread_id = await read_thread_id(user_id)
    if thread_id:
        await destroy_thread(user_id, thread_id)
    await update.message.reply_text("Context cleared")


async def photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    best_photo = max(update.message.photo, key=lambda x: x.width * x.height)
    photo_file = await best_photo.get_file()
    b64_photo = await encode_photo_file_to_base64(photo_file)
    answer = await get_vision_response(update.message.caption, b64_photo)
    await update.message.reply_text(answer)


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = await get_location_completion(update.message)
    await update.message.reply_text(answer)


async def chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    answer = await send_thread_message(user_id, update.message.text)
    await update.message.reply_text(answer)
