from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from npb import strings
from npb.openai import (
    destroy_thread,
    get_location_completion,
    get_vision_response,
    send_thread_message,
)
from npb.s3 import read_thread_id
from npb.utils import encode_photo_file_to_base64


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(strings.start_command_response)


async def delcontext_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    thread_id = await read_thread_id(user_id)
    if thread_id:
        await destroy_thread(user_id, thread_id)
    await update.message.reply_text(strings.context_cleared)


async def photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_chat_action(action=ChatAction.TYPING)
    best_photo = max(update.message.photo, key=lambda x: x.width * x.height)
    photo_file = await best_photo.get_file()
    b64_photo = await encode_photo_file_to_base64(photo_file)
    answer = await get_vision_response(update.message.caption, b64_photo)
    await send_thread_message(
        update.effective_user.id,
        f"{strings.add_vision_context}{answer}",
        run_thread=False,
    )
    await update.message.reply_text(answer)


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_chat_action(action=ChatAction.TYPING)
    answer = await get_location_completion(update.message)
    await update.message.reply_text(answer)


async def chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_chat_action(action=ChatAction.TYPING)
    user_id = update.message.from_user.id
    answer = await send_thread_message(user_id, update.message.text)
    await update.message.reply_text(answer)
