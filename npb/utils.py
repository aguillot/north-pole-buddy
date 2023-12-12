import base64
import io

from telegram import File


async def encode_photo_file_to_base64(file: File):
    buffer = io.BytesIO()
    await file.download_to_memory(buffer)
    buffer.seek(0)
    b64_photo = base64.b64encode(buffer.read()).decode("utf-8")
    return b64_photo


async def get_gpt_vision_payload(
    encoded_photo, prompt, extra_prompt="", model="gpt-4-vision-preview", max_tokens=300
):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt + extra_prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_photo}"},
                    },
                ],
            }
        ],
        "max_tokens": max_tokens,
    }
    return payload
