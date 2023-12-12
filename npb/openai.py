import asyncio
import os
import random

import httpx
from loguru import logger
from openai import Client
from telegram import Message

from npb import s3
from npb.utils import get_gpt_vision_payload

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID", "")
COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}

LOCATION_PROMPTS = [
    """
    Based on the gps coordinates provided by the user, Give me a funny christmas story about the location of the user.
    When you reply, don't mention the gps coordinates. But you can mention the town name or the region name

    The user localisation is: {coords}
    """,
    """
    Based on the gps coordinates provided by the user, create a list of 10 christmas gift based and culture, tradition and specialty for that area.
    When you reply, don't mention the gps coordinates but the town or region of the user.

    The user localisation is: {coords}
    """,
    """
    Based on the gps coordinates provided by the user, suggest somes places to visit for that region.
    Theses places must have a link to christmas
    When you reply, don't mention the gps coordinates but the town or region of the user.

    The user localisation is: {coords}
    """,
]

EXTRA_PROMPT = "Act and respond in the voice and tone of Santa Claus"

client = Client()


async def get_vision_response(prompt: str, encoded_photo: str) -> str:
    payload = await get_gpt_vision_payload(encoded_photo, prompt, EXTRA_PROMPT)
    async with httpx.AsyncClient() as client:
        timeout = httpx.Timeout(25.0, read=None)
        response = await client.post(
            COMPLETIONS_URL, headers=HEADERS, json=payload, timeout=timeout
        )
        json_response = response.json()
    if response.is_success:
        answer = json_response["choices"][0]["message"]["content"]
        return answer
    else:
        logger.warning(
            f"cannot get image description, {response.status_code=}, {json_response}"
        )
        return "Cannot see"


async def get_location_completion(message: Message) -> str:
    coords = f"{message.location.latitude}, {message.location.longitude}"
    prompt = random.choice(LOCATION_PROMPTS).format(coords=coords)
    answer = await send_thread_message(message.from_user.id, prompt)
    return answer


async def get_thread_id(user_id: int) -> str:
    thread_id = await s3.read_thread_id(user_id)
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
        await s3.write_thread_id(user_id, thread_id)
    return thread_id


async def destroy_thread(user_id: int, thread_id: str):
    await s3.delete_thread_id(user_id)
    client.beta.threads.delete(thread_id)


async def send_thread_message(user_id: int, message: str) -> str:
    thread_id = await get_thread_id(user_id)
    client.beta.threads.messages.create(thread_id, content=message, role="user")
    run = client.beta.threads.runs.create(thread_id, assistant_id=OPENAI_ASSISTANT_ID)
    while (
        client.beta.threads.runs.retrieve(run.id, thread_id=thread_id).status
        != "completed"
    ):
        await asyncio.sleep(1.0)
    messages = client.beta.threads.messages.list(thread_id)
    latest_answer = messages.data[0].content[0].text.value
    return latest_answer
