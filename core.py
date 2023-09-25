import asyncio
import json
import subprocess
from io import BytesIO

from aiogram import Bot, Dispatcher, F
from aiogram.types import BufferedInputFile, Message
from decouple import Csv, config
from PIL import Image, ImageDraw, ImageFont

COMMANDS = json.load(open("./commands.json"))


def generate_image(
    log: str,
    bytesIO: BytesIO,
    line_height: int = 20,
    padding: int = 25,
    font_size: int = 15,
    image_width_ratio: int = 10,
    background: str = '#181818',
    color: str = '#ea9e57',
):
    # Set up font
    font = ImageFont.truetype("Hack-Bold.ttf", font_size)
    # Calculate image height based on number of lines
    lines: list[str] = log.split('\n')

    image_height = (len(lines) * line_height) + (2 * padding)
    image_width = max(len(line) for line in lines) * image_width_ratio

    # Create a blank image with background color
    image = Image.new('RGB', (image_width, image_height), color=background)
    draw = ImageDraw.Draw(image)

    # Draw text on the image
    y = padding
    for line in lines:
        draw.text((padding, y), line, font=font, fill=color)
        y += line_height

    # Save the image to bytesIO
    image.save(bytesIO, format='PNG')


# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(F.from_user.id.in_(config("ADMINS", cast=Csv(int))))
async def echo_handler(message: Message) -> None:
    if not message.text.startswith("/run "):
        return message.answer("no command detected.")

    run = message.text.lstrip("/run ").lower()
    cmd = next((cmd["command"] for cmd in COMMANDS if run == cmd["name"]), None)

    if not cmd:
        return message.answer("no command found.")

    subprocess.call(f'echo "{cmd}" > /hostpipe/exec_in.pipe', shell=True)
    log = subprocess.check_output(['cat', '/hostpipe/exec_out.pipe'], text=True)

    with BytesIO() as bytesIO:
        # generate image from log and save into memory
        generate_image(log, bytesIO)
        # reply generated image to admin without saving into storage
        await message.reply_photo(
            BufferedInputFile(bytesIO.getvalue(), filename="TEMP.PNG")
        )


async def main() -> None:
    # Initialize Bot instance and run events dispatching
    await dp.start_polling(Bot(config("TOKEN")))


if __name__ == "__main__":
    asyncio.run(main())
