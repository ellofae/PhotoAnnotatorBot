# Polaroid-Converter-Py

____
Запуск бота: python main.py

* Пример .env файла:

API_TOKEN={BOT_TOKEN}

PADDING_TOP = 15
PADDING_BOTTOM = 15
PADDING_LEFT = 15

TEXT_COLOR = #ffff00
BACKGROUND_COLOR = #000000
FONT_NAME = arial
FONT_COEFFICIENT = 1

____
Запуск утилиты отдельно(при использовании sys.args): python main.py {image_name}.{format} {user_name} {text:OPTIONAL}
* {text} является опциональным, если не указан, то текст используется по умолчанию.
_____
Примеры запуска отдельно (при использовании sys.args):
* python main.py main.png bykovskiy
* python main.py main3.jpg bykovskiy 'Блок 1. Дверь в тренерскую'

_____
Структура проекта:

* Фото для обработки находятся в images
* Результаты обработки фото находятся в results
* Шрифты находятся в fonts, переменная font_name отвечает за используемый шрифт (источник шрифтов: https://fonts.google.com/)
