import os
import tempfile
import random
import string

from decouple import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, InputFile
from datetime import datetime

from image_service.main import start_processing

API_TOKEN = config('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
filename_chars_amount = 14

def generate_random_filename(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAMhZNzq4JtQw4N5vyF_orR_VbvQdyoAAtgPAAJI8mBLFfvE2nh0a5gwBA')
    await message.reply('Привет! Отправь фото и текст :)')

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    current_user = message.from_user.username
    
    caption_text = message.caption
    if not caption_text:
        await message.answer("Ошибка: подпись к фото отсутствует")
        return

    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file.file_path)
    
    file_extension = os.path.splitext(file.file_path)[-1]
    temp_file_name = generate_random_filename(filename_chars_amount) + file_extension
    
    with tempfile.NamedTemporaryFile(suffix=file_extension, prefix=temp_file_name, delete=False) as temp_file:
        try:
            temp_file.write(downloaded_file.read())
            temp_file.seek(0)
            
            processed_file_path = start_processing(temp_file.name, current_user, caption_text)
            
            with open(processed_file_path, "rb") as photo_file:
                photo_input = InputFile(photo_file)
                await message.answer_photo(photo=photo_input)
        finally:
            temp_file.close()
            os.unlink(temp_file.name)
            os.unlink(processed_file_path)
    

if __name__ == '__main__':
   print(datetime.now().strftime('%Y-%m-%d %H:%M'))
   executor.start_polling(dp, skip_updates=True)