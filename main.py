import textwrap
import sys

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

    
def add_message(image, text, font, text_color, text_start_height, fontsize, spacing, padding_left):
    draw_img = ImageDraw.Draw(image)
    y_text = text_start_height
    lines = textwrap.wrap(text, width=image.width // 10)
    
    for line in lines:
        draw_img.text((padding_left, y_text), 
                  line, font=font, fill=text_color)
        y_text += fontsize*spacing
        
    return y_text

def make_wrapper(fontsize, text, image, spacing, padding_bottom):
    sender_mark_space = 40 + padding_bottom
    
    lines = textwrap.wrap(text, width=image.width // 10)
    
    extra_bound_size = 0
    for _ in lines:
        extra_bound_size += fontsize*spacing
    extra_bound_size += sender_mark_space
        
    wrapper = Image.new("RGB", (image.width, image.height + int(extra_bound_size)), "black")
    wrapper.paste(image, (0,0))
    
    return wrapper, extra_bound_size

def sender_mark(image_wrapper, message_sender, text_start, font, text_color, fontsize, spacing, padding_left):
    current_time = datetime.now()
    
    date = current_time.strftime('%Y-%m-%d')
    timer = current_time.strftime('%H:%M')
    
    text =  f'@{message_sender}, {date}, {timer}'
    lines = textwrap.wrap(text, width=image_wrapper.width//10)
    
    draw_img = ImageDraw.Draw(image_wrapper)
    
    y_text = text_start
    for line in lines:
        draw_img.text((padding_left, y_text), 
                  line, font=font, fill=text_color)
        y_text += fontsize*spacing

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
    spacing = 1
    
    image = Image.open(f'./images/{image_name}')
    
    image_wrapper, bound_size = make_wrapper(fontsize, text, image, spacing, padding_bottom)
    text_start_height = image_wrapper.height - int(bound_size) + padding_top
    
    text_end_line = add_message(image_wrapper, text, font, text_color, text_start_height, fontsize, spacing, padding_left)
    sender_mark(image_wrapper, message_sender, text_end_line + padding_top, font, text_color, fontsize, spacing, padding_left)
    
    image_wrapper.save(f'./results/{image_name}')

    
if __name__ == "__main__":
    main()