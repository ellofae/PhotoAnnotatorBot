from decouple import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message, InputFile

from image_service.main import start_processing, delete_stored_image

API_TOKEN = config('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAMhZNzq4JtQw4N5vyF_orR_VbvQdyoAAtgPAAJI8mBLFfvE2nh0a5gwBA')
    await message.reply('Привет! Отправь фото и текст :)')


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    current_user = message.from_user.username

    photo = message.photo[-1]

    caption_text = message.caption
    if not caption_text:
        await message.answer("Ошибка: подпись к фото отсутствует")
        return

    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    file_info = await photo.get_file()

    file_extension = file_info.file_path.split(".")[-1]
    file_name = photo.file_id + '.' + file_extension
    await bot.download_file(file_path, './image_service/images/' + file_name)

    start_processing(file_name, current_user, caption_text)

    with open('./image_service/results/' + file_name, "rb") as photo_file:
        photo_input = InputFile(photo_file)
        await message.answer_photo(photo=photo_input)

    delete_stored_image(file_name)




if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)