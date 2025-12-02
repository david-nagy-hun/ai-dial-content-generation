import asyncio
import uuid
from datetime import datetime

from task._models.custom_content import Attachment
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role

class Size:
    """
    The size of the generated image.
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    The style of the generated image. Must be one of vivid or natural.
     - Vivid causes the model to lean towards generating hyper-real and dramatic images.
     - Natural causes the model to produce more natural, less hyper-real looking images.
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    The quality of the image that will be generated.
     - ‘hd’ creates images with finer details and greater consistency across the image.
    """
    standard: str = "standard"
    hd: str = "hd"

async def _save_images(attachments: list[Attachment]):
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as client:
        for attachment in attachments:
            if attachment.type and attachment.type == 'image/png':
                image_bytes = await client.get_file(attachment.url)
                filename = f'{uuid.uuid4()}.png'

                with open(filename, 'wb') as f:
                    f.write(image_bytes)

                print(f"Image saved to {filename}")


def start() -> None:
    client = DialModelClient(endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT, deployment_name="dall-e-3", api_key=API_KEY)
    user_input = "Sunny day on Bali"
    message = Message(Role.USER, user_input)
    custom_fields = {
        "size": Size.square,
        "style": Style.vivid,
        "quality": Quality.standard
    }

    response = client.get_completion([message], custom_fields)

    if custom_content := response.custom_content:
        if attachments := custom_content.attachments:
            asyncio.run(_save_images(attachments))


start()
