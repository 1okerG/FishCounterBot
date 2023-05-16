from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

stats_category_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('За цей місяць \U0001F4C8', callback_data='per_month'),
        InlineKeyboardButton('Обрати місяць \U0001F4D2', callback_data='by_months'),
    ],
    [
        InlineKeyboardButton('За цей рік \U0001F4C9', callback_data='per_year'),
        InlineKeyboardButton('Обрати рік \U0001F4C6', callback_data='by_years'),
    ],
])

month_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Січень \U0001F976', callback_data='1'),
        InlineKeyboardButton('Лютий \U0001F32C', callback_data='2'),
        InlineKeyboardButton('Березень \U0001F337', callback_data='3')
    ],
    [
        InlineKeyboardButton('Квітень \U0001F33F', callback_data='4'),
        InlineKeyboardButton('Травень \U0001FAB8', callback_data='5'),
        InlineKeyboardButton('Червень \U0001F975', callback_data='6')
    ],
    [
        InlineKeyboardButton('Липень \U0001F33E', callback_data='7'),
        InlineKeyboardButton('Серпень \U0001F33B', callback_data='8'),
        InlineKeyboardButton('Вересень \U0001F3EB', callback_data='9')
    ],
    [
        InlineKeyboardButton('Жовтень \U0001F341', callback_data='10'),
        InlineKeyboardButton('Листопад \U0001F344', callback_data='11'),
        InlineKeyboardButton('Грудень \U0001F384', callback_data='12')
    ]
])