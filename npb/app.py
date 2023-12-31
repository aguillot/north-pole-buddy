import os
from typing import Union

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from loguru import logger
from telegram import Update

from npb import strings
from npb.tgapp import tg_app

TELEGRAM_SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN", "")

app = FastAPI()


async def verify_telegram_secret_token(
    x_telegram_bot_api_secret_token: Union[str, None] = Header(None)
):
    if x_telegram_bot_api_secret_token != TELEGRAM_SECRET_TOKEN:
        logger.warning("received request with wrong secret token")
        raise HTTPException(status_code=401, detail=strings.wrong_token)


@app.post("/", dependencies=[Depends(verify_telegram_secret_token)])
async def telegram_webhook(request: Request):
    data = await request.json()
    try:
        update = Update.de_json(data, tg_app.bot)
    except TypeError:
        raise HTTPException(status_code=400, detail=strings.cannot_serialize)
    logger.debug(f"received update {update}")
    try:
        await tg_app.initialize()
        await tg_app.process_update(update)
    finally:
        await tg_app.shutdown()
    return {"status": "ok"}
