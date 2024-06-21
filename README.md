# PhotoAnnotatorBot

A bot based on the aiogram library is an ideal tool for image processing. The bot allows you to add text to an image to make it more informative.
The user can upload any image in Telegram and write any text and the bot will instantly return the processed image with added text.

The utility for adding text to images is written in Python using the Pillow library. You can quickly and easily add text to images, making them more informative and expressive.
Thanks to the use of the powerful Pillow library, the utility allows you to perform a wide range of text operations such as resizing, font, color and style selection.

## Ways to launch the bot: 

* Docker: `./docker.sh` or `docker-compose up`
* Direct: `python main.py` (requirements.txt should be processed before)

## Configuration

add the `.env` file:

```
API_TOKEN={BOT_TOKEN}
PADDING_TOP=15
PADDING_BOTTOM=15
PADDING_LEFT=15
TEXT_COLOR=#ffff00
BACKGROUND_COLOR=#000000
FONT_NAME=arial
FONT_COEFFICIENT=1
```
