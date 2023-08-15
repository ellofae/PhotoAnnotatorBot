import textwrap
import math
import sys

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

font_chars = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯяabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def get_text_wrapper(font, image, text):
    avg_chat_width = sum(font.getbbox(char)[2] for char in font_chars) / len(font_chars)
    max_char_count = int((image.size[0] * .95) / avg_chat_width )
    text = textwrap.fill(text=text, width=max_char_count)
    
    return text, max_char_count

def add_message(image, text, font, text_color, text_start_height, fontsize, spacing, padding_left):
    draw_img = ImageDraw.Draw(image)
    y_text = text_start_height
    
    # text = textwrap.fill(text=text, width=60)
    # print(text)
    #
    #
    # avg_chat_width = sum(font.getbbox(char)[2] for char in font_chars) / len(font_chars)
    # max_char_count = int((image.size[0] * .95) / avg_chat_width )
    # text = textwrap.fill(text=text, width=max_char_count)
    text, max_char_count = get_text_wrapper(font, image, text)
    draw_img.text((padding_left, y_text), text, font=font, fill=text_color, align='left')
    
    # lines = textwrap.wrap(text, width=image.width // 10)
    
    # for line in lines:
    #     draw_img.text((padding_left, y_text), 
    #               line, font=font, fill=text_color)
    #     y_text += fontsize*spacing
        
    #return y_text
    print(y_text + fontsize*spacing*math.ceil((len(text) / max_char_count)))
    return y_text + fontsize*spacing * math.ceil((len(text) / max_char_count))
    
def get_marking_data(message_sender):
    current_time = datetime.now()
    
    date = current_time.strftime('%Y-%m-%d')
    timer = current_time.strftime('%H:%M')
    
    text = f'@{message_sender}, {date}, {timer}'
    return text

def get_extra_space_size(message_sender, font, image, fontsize, spacing):
    text = get_marking_data(message_sender)
    text, max_char_count = get_text_wrapper(font, image, text)
    
    return fontsize*spacing * math.ceil((len(text) / max_char_count)) * 3
    

def make_wrapper(font, fontsize, text, image, spacing, padding_bottom, padding_top, extra_space_size):
    sender_mark_space = extra_space_size + padding_bottom + padding_top
    
    #lines = textwrap.wrap(text, width=image.width // 10)
    
    text, max_char_count = get_text_wrapper(font, image, text)
    #extra_bound_size = 0
    # for _ in lines:
    #     extra_bound_size += fontsize*spacing
    extra_bound_size = sender_mark_space + fontsize*spacing * math.ceil((len(text) / max_char_count))
        
    wrapper = Image.new("RGB", (image.width, image.height + int(extra_bound_size)), "black")
    wrapper.paste(image, (0,0))
    
    return wrapper, extra_bound_size



def sender_mark(image_wrapper, message_sender, text_start, font, text_color, padding_left, fontsize,spacing):
    #current_time = datetime.now()
    #text_top_padding = 5
    
    # date = current_time.strftime('%Y-%m-%d')
    # timer = current_time.strftime('%H:%M')
    
    # text = f'@{message_sender}, {date}, {timer}'
    text = get_marking_data(message_sender)
    #lines = textwrap.wrap(text, width=image_wrapper.width//10)
    
    draw_img = ImageDraw.Draw(image_wrapper)
    
    #y_text = text_start # + text_top_padding
    # for line in lines:
    #     draw_img.text((padding_left, y_text), 
    #               line, font=font, fill=text_color)
    #     y_text += fontsize*spacing
    text, max_char_count = get_text_wrapper(font, image_wrapper, text)
    y_text = text_start + fontsize*spacing * math.ceil((len(text) / max_char_count))
    
    draw_img.text((padding_left, y_text), text, font=font, fill=text_color, align='left')

# def get_dynamic_fontsize(image, text, font_name):
#     font_size = 1
#     font = ImageFont.truetype(f"./fonts/{font_name}.ttf", font_size)
#     print("size:", image.width)
#     print(font.getbbox(text))
#     while font.getbbox(text)[2] < image.width:
#         print(font.getbbox(text)[2])
#         font_size += 1
#         font = ImageFont.truetype(f"./fonts/{font_name}.ttf", font_size)
#     font_size -= 1
#     print(font_size)

#     return font, font_size

def main():
    image_name = sys.argv[1]
    message_sender = sys.argv[2]
    text = ""
    if len(sys.argv) == 4:
        text = sys.argv[3]
    else:
        text = 'Блок 1. Дверь в тренерское помещение. Дверь не соотвутствует размерам в спецификации. Составить акт, и в случае косяка производителя - написать претензию'
    
    fontsize = 16
    font_name = 'robotomono-bold'
    font = ImageFont.truetype(f"./fonts/{font_name}.ttf", fontsize)
    text_color = (255,255,0)
    padding_top = 10
    padding_bottom = 10
    padding_left = 15
    text_top_padding = 10
    spacing = 1
    
    image = Image.open(f'./images/{image_name}')
    #font, fontsize = get_dynamic_fontsize(image, text, font_name)
    
    extra_space_size = get_extra_space_size(message_sender, font, image, fontsize, spacing)
    
    image_wrapper, bound_size = make_wrapper(font, fontsize, text, image, spacing, padding_bottom, padding_top, extra_space_size)
    text_start_height = image_wrapper.height - int(bound_size) + padding_top
    
    text_end_line = add_message(image_wrapper, text, font, text_color, text_start_height, fontsize, spacing, padding_left)
    sender_mark(image_wrapper, message_sender, text_end_line + text_top_padding, font, text_color, padding_left, fontsize, spacing)
    
    image_wrapper.save(f'./results/{image_name}')

    
if __name__ == "__main__":
    main()