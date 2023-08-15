import textwrap
import sys

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

    
def add_message(image, text, font, text_color, text_start_height, fontsize, spacing):
    padding_left = 20
    
    draw_img = ImageDraw.Draw(image)
    #image_width, _ = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=image.width//10)
    
    for line in lines:
        #line_width = font.getlength(line)
        # (image_width - line_width) / 2
        draw_img.text((padding_left, y_text), 
                  line, font=font, fill=text_color)
        y_text += fontsize*spacing

def make_wrapper(fontsize, text, image, spacing):
    # image.width//10
    sender_mark_space = 40
    
    lines = textwrap.wrap(text, width=image.width//10)
    
    extra_bound_size = 0
    for _ in lines:
        extra_bound_size += fontsize*spacing
    extra_bound_size += sender_mark_space
        
    wrapper = Image.new("RGB", (image.width, image.height + int(extra_bound_size)), "black")
    wrapper.paste(image, (0,0))
    
    return wrapper, extra_bound_size

# def sender_mark(image_wrapper, message_sender):
#     current_time = datetime.now()
    
def main():
    image_name = sys.argv[1]
    message_sender = sys.argv[2]
    text = ""
    if len(sys.argv) == 4:
        text = sys.argv[3]
    else:
        text = 'Блок 1. Дверь в тренерское помещение. Дверь не соотвутствует размерам в спецификации. Составить акт, и в случае косяка производителя - написать претензию'
    
    fontsize = 16
    font = ImageFont.truetype("./fonts/arial.ttf", fontsize)
    text_color = (255,255,0)
    padding_top = 8
    spacing = 1
    
    
    image = Image.open(f'./images/{image_name}')
    
    image_wrapper, bound_size = make_wrapper(fontsize, text, image, spacing)
    text_start_height = image_wrapper.height - int(bound_size) + padding_top
    
    add_message(image_wrapper, text, font, text_color, text_start_height, fontsize, spacing)
   # sender_mark(image_wrapper, message_sender)
    
    image_wrapper.save(f'./results/{image_name}')

    
if __name__ == "__main__":
    main()