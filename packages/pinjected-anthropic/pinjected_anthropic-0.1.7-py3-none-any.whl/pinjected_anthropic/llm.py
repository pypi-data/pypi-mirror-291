import base64
import io
from collections import defaultdict
from dataclasses import dataclass
from typing import Literal

from anthropic import AsyncAnthropic, Stream
from anthropic.types import Message, MessageStartEvent, ContentBlockStartEvent, ContentBlockDeltaEvent, MessageParam
from pinjected import *
from anthropic.types.image_block_param import ImageBlockParam, Source
from PIL import Image
import PIL
import httpx
from anthropic import RateLimitError,InternalServerError
import asyncio


@instance
async def anthropic_client(anthropic_api_key):
    return AsyncAnthropic(api_key=anthropic_api_key)


IMAGE_FORMAT = Literal['jpeg', 'png']


@injected
async def a_anthropic_llm(
        anthropic_client,
        /,
        messages: list[dict],
        max_tokens=1024,
        # model="claude-3-opus-20240229"
        model="claude-3-5-sonnet-20240620"
) -> Message:
    msg = await anthropic_client.messages.create(
        max_tokens=max_tokens,
        model=model,
        messages=messages
    )
    return msg


def image_to_base64(image: PIL.Image.Image, fmt: IMAGE_FORMAT) -> str:
    assert isinstance(image, PIL.Image.Image), f"image is not an instance of PIL.Image.Image: {image}"
    bytes_io = io.BytesIO()
    image.save(bytes_io, format=fmt)
    bytes_io.seek(0)
    data = base64.b64encode(bytes_io.getvalue()).decode('utf-8')
    assert data, "data is empty"
    return data


"""


import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image1_media_type,
                        "data": image1_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)
print(message)
"""


@instance
async def anthropic_rate_limit_locks_lock():
    return asyncio.Lock(),defaultdict(asyncio.Lock)
@injected
async def anthropic_rate_limit_locks(anthropic_rate_limit_locks_lock,/,key):
    lock,locks = anthropic_rate_limit_locks_lock
    async with lock:
        return locks[key]


@injected
async def a_vision_llm__anthropic(
        anthropic_client: AsyncAnthropic,
        image_to_base64,
        logger,
        anthropic_rate_limit_locks,
        /,
        text: str,
        images: list[PIL.Image.Image] = None,
        model="claude-3-opus-20240229",
        max_tokens: int = 2048,
        img_format: IMAGE_FORMAT = 'jpeg'
) -> str:
    img_blocks = []
    if images is not None:
        for img in images:
            block = {
                'type': 'image',
                'source': {
                    'type': 'base64',
                    'media_type': f"image/{img_format}",
                    'data': image_to_base64(img, img_format),
                }
            }
            img_blocks.append(block)

    async def attempt():
        msg = await anthropic_client.messages.create(
            model=model,
            messages=[
                {
                    'content': [
                        *img_blocks,
                        {
                            'type': 'text',
                            'text': text
                        },
                    ],
                    'role': "user"
                },
            ],
            max_tokens=max_tokens
        )
        msg: Message
        return msg

    while True:
        try:
            resp = await attempt()
            return resp.content[-1].text
        except RateLimitError as rle:
            async with (await anthropic_rate_limit_locks(model)):
                logger.warning(f"Rate limit error for model {model}, waiting for {5} seconds")
                await asyncio.sleep(5)
        except InternalServerError as ise:
            async with (await anthropic_rate_limit_locks(model)):
                logger.warning(f"Rate limit error for model {model}, waiting for {5} seconds")
                await asyncio.sleep(10)



@injected
async def a_anthropic_llm_stream(
        anthropic_client,
        /,
        messages: list[dict],
        max_tokens=1024,
        model="claude-3-opus-20240229"
) -> Stream:
    msg = await anthropic_client.messages.create(
        max_tokens=max_tokens,
        model=model,
        messages=messages,
        stream=True
    )
    async for item in msg:
        match item:
            case MessageStartEvent():
                pass
            case ContentBlockStartEvent():
                pass
            case ContentBlockDeltaEvent() as cbde:
                yield cbde.delta.text


test_run_opus: Injected = a_anthropic_llm(
    messages=[
        {
            "content": "What is the meaning of life?",
            "role": "user"
        }
    ],
)

test_a_vision_llm: IProxy = a_vision_llm__anthropic(
    text="What is the meaning of life?",
    images=[],
)
sample_image = injected(Image.open)("test_image/test1.jpg")
test_to_base64: IProxy = injected(image_to_base64)(sample_image, 'jpeg')
test_a_vision_llm_with_image: IProxy = a_vision_llm__anthropic(
    text="What do you see in this image?",
    images=Injected.list(
        injected(Image.open)("test_image/test1.jpg")
    ),
)


@instance
async def test_run_opus_stream(a_anthropic_llm_stream):
    stream = a_anthropic_llm_stream(
        messages=[
            {
                "content": "What is the meaning of life?",
                "role": "user"
            }
        ],
    )
    async for msg in stream:
        print(msg)


__meta_design__ = instances(

)
