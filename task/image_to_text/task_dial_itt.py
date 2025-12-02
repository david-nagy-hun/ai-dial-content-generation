import asyncio
from io import BytesIO
from pathlib import Path
from tkinter import image_names

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


async def _put_image() -> Attachment:
    file_name = 'dialx-banner.png'
    image_path = Path(__file__).parent.parent.parent / file_name
    mime_type_png = 'image/png'

    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as client:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        image_content = BytesIO(image_bytes)

        response = await client.put_file(file_name, mime_type_png, image_content)

        return Attachment(
            title=file_name,
            url=response.get('url'),
            type=mime_type_png,
        )


def start() -> None:
    client = DialModelClient(endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT, deployment_name="gpt-4o", api_key=API_KEY)

    attachment = asyncio.run(_put_image())
    print(attachment)

    content = "What do you see on this picture?"
    custom_content = CustomContent([attachment])
    message = Message(Role.USER, content, custom_content)
    client.get_completion([message])


start()
