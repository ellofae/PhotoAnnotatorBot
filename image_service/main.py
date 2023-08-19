import os
import textwrap
import tempfile
from datetime import datetime
from decouple import config

from PIL import Image, ImageDraw, ImageFont


def get_box_sizes(text, font):
    (width, baseline), _ = font.font.getsize(text)

    return baseline

def get_message_data(message_sender):
    current_time = datetime.now()

    date = current_time.strftime('%Y-%m-%d %H:%M')

    text = f'@{message_sender}, {date}'
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


def get_dynamic_textwrap_width(text, font, max_width):
    temp = text.split()

    line = ''
    for word in temp:
        (width, _), _ = font.font.getsize(line + ' ' + word)

        if width > max_width - 100:
            return len(line)
        else:
            line += ' ' + word if len(line) != 0 else word


    return len(line)

def make_text_wrapper(main_text, sender_text, font, image, text_color, background_color, padding_left, padding_top, padding_bottom):
    main_lines = textwrap.wrap(main_text, width=get_dynamic_textwrap_width(main_text, font, image.width))
    sender_lines = textwrap.wrap(sender_text, width=get_dynamic_textwrap_width(sender_text, font, image.width))

    main_lines_height = 0
    for line in main_lines:
        main_lines_height += get_box_sizes(line, font)

    sender_lines_height = 0
    for line in sender_lines:
        sender_lines_height += get_box_sizes(line, font)

    sum_heights = main_lines_height + sender_lines_height
    all_paddings = padding_top * 2 + padding_bottom
    wrapper = Image.new("RGB", (image.width, sum_heights + all_paddings), background_color)

    end_height = add_main_text(main_lines, font, text_color, wrapper, padding_left, 0, padding_top)
    add_sender_text(sender_lines, font, text_color, wrapper, padding_left, end_height, padding_top)

    return wrapper

def combine_images(image, text_wrapper):
    image_wrapper = Image.new("RGB", (image.width, image.height + text_wrapper.height), "white")
    image_wrapper.paste(image, (0, 0))
    image_wrapper.paste(text_wrapper, (0, image.height))

    return image_wrapper

def start_processing(image_name, message_sender, text):
    koef = float(config('FONT_COEFFICIENT'))
    font_name = config('FONT_NAME')
    text_color = config('TEXT_COLOR')
    background_color = config('BACKGROUND_COLOR')
    padding_left = int(config('PADDING_LEFT'))
    padding_top = int(config('PADDING_TOP'))
    padding_bottom = int(config('PADDING_BOTTOM'))

    image = Image.open(image_name)

    fontsize = image.size[0] * 0.02 * koef
    if fontsize < 12:
        fontsize = 12
    font = ImageFont.truetype(f"./image_service/fonts/{font_name}.ttf", fontsize)

    sender_text = get_message_data(message_sender)

    text_wrapper = make_text_wrapper(text, sender_text, font, image, text_color, background_color, padding_left, padding_top, padding_bottom)
    resulting_image = combine_images(image, text_wrapper)

    file_base_name = os.path.basename(image_name)
    file_name, extension = os.path.splitext(file_base_name)
    
    processed_filepath = ''
    with tempfile.NamedTemporaryFile(suffix=extension,prefix=f'processed_{file_name}', delete=False) as temp_file:
        try:
            resulting_image.save(temp_file.name)
            temp_file.seek(0)
            processed_filepath = temp_file.name
        finally:
            temp_file.close()
    
    return processed_filepath