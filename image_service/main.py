import textwrap
import math
import sys

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def get_box_sizes(text, font):
    (width, baseline), _ = font.font.getsize(text)

    return baseline

def get_message_data(message_sender):
    current_time = datetime.now()

    date = current_time.strftime('%Y-%m-%d')
    timer = current_time.strftime('%H:%M')

    text = f'@{message_sender}, {date}, {timer}'
    return text

def add_main_text(text, font, text_color, image, padding_left, start_position, padding_top):
    draw_img = ImageDraw.Draw(image)
    y_text = start_position + padding_top

    for line in text:
        draw_img.text((padding_left, y_text),
              line, font=font, fill=text_color)
        y_text += get_box_sizes(line, font)

    return y_text

def add_sender_text(text, font, text_color, image, padding_left, start_position, padding_top):
    draw_img = ImageDraw.Draw(image)
    y_text = start_position + padding_top

    for line in text:
        draw_img.text((padding_left, y_text),
                      line, font=font, fill=text_color)
        y_text += get_box_sizes(line, font)

def make_text_wrapper(main_text, sender_text, font, image, text_color, padding_left, padding_top):
    main_lines = textwrap.wrap(main_text)
    sender_lines = textwrap.wrap(sender_text)

    main_lines_height = 0
    for line in main_lines:
        main_lines_height += get_box_sizes(line, font)

    sender_lines_height = 0
    for line in sender_lines:
        sender_lines_height += get_box_sizes(line, font)

    sum_heights = main_lines_height + sender_lines_height
    all_paddings = padding_top * 2
    wrapper = Image.new("RGB", (image.width, sum_heights + all_paddings), "black")

    end_height = add_main_text(main_lines, font, text_color, wrapper, padding_left, 0, padding_top)
    add_sender_text(sender_lines, font, text_color, wrapper, padding_left, end_height, padding_top)

    return wrapper

def combine_images(image, text_wrapper):
    image_wrapper = Image.new("RGB", (image.width, image.height + text_wrapper.height), "white")
    image_wrapper.paste(image, (0, 0))
    image_wrapper.paste(text_wrapper, (0, image.height))

    return image_wrapper

def start_processing(image_name, message_sender, text):
    # image_name = sys.argv[1]
    # message_sender = sys.argv[2]
    # text = ""
    # if len(sys.argv) == 4:
    #     text = sys.argv[3]
    # else:
    #     text = 'Блок 1. Дверь в тренерское помещение. Дверь не соотвутствует размерам в спецификации. Составить акт, и в случае косяка производителя - написать претензию'
    if len(text) == 0:
        text = 'Блок 1. Дверь в тренерское помещение. Дверь не соотвутствует размерам в спецификации. Составить акт, и в случае косяка производителя - написать претензию'

    font_name = 'arial'
    text_color = (255, 255, 0)
    padding_left = 15
    padding_top = 15

    image = Image.open(f'./image_service/images/{image_name}')

    fontsize = image.size[0] * 0.02
    if fontsize < 12:
        fontsize = 12
    font = ImageFont.truetype(f"./image_service/fonts/{font_name}.ttf", fontsize)

    sender_text = get_message_data(message_sender)

    text_wrapper = make_text_wrapper(text, sender_text, font, image, text_color, padding_left, padding_top)
    resulting_image = combine_images(image, text_wrapper)

    resulting_image.save(f'./image_service/results/{image_name}')