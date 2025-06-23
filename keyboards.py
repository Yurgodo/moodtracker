from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(
    KeyboardButton('📌 Добавить событие дня'),
    KeyboardButton('✏️ Изменить событие дня'),
)
main_kb.add(
    KeyboardButton('📆 Посмотреть события недели'),
    KeyboardButton('🌟 Посмотреть лучшие события недели'),
)
main_kb.add(
    KeyboardButton('🏆 Посмотреть лучшие события месяца')
)
