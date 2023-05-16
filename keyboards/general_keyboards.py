from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('\U0001F6F3 Я Починаю | Продовжую риболовлю', callback_data='add_info'),
    ],
    [
        InlineKeyboardButton('\U0001F4C5 Додати інформацію за минулі дати', callback_data='add_past_info'),
    ],
    [
        InlineKeyboardButton('\U0001F4CA Переглянути свою статистику', callback_data='stats'),
    ],
    [
        InlineKeyboardButton('\U0001F4DA FAQ', callback_data='faq'),
        InlineKeyboardButton("\u260E\ufe0e Зворотній зв'язок", callback_data='callback'),
    ],
])

confirm_keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Так \U0001F60E', callback_data='add_info'),
        InlineKeyboardButton('Ні \U0001F625', callback_data='no_fishing'),
    ],
    [
        InlineKeyboardButton('Меню \U0001F4F1', callback_data='menu'),
    ],
])

