from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# In aiogram v3, ReplyKeyboardMarkup expects the keyboard layout to be
# provided on initialization. The previous approach using ``add``
# corresponds to the old builder API from aiogram v2 and leads to a
# validation error.  Here we explicitly pass the keyboard structure as a
# nested list of ``KeyboardButton`` objects.

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📌 Добавить событие дня'),
            KeyboardButton(text='✏️ Изменить событие дня'),
        ],
        [
            KeyboardButton(text='📆 Посмотреть события недели'),
            KeyboardButton(text='🌟 Посмотреть лучшие события недели'),
        ],
        [
            KeyboardButton(text='🏆 Посмотреть лучшие события месяца'),
        ],
    ],
    resize_keyboard=True,
)
