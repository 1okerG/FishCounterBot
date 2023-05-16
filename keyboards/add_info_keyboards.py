from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm_keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Звісно \U0001F60E', callback_data='start_dialog'),
        InlineKeyboardButton('На жаль, ні \U0001F610', callback_data='no_catch_fish')
    ],
    [
        InlineKeyboardButton('Повернутись до меню \U0001F4F1', callback_data='menu'),
    ],
])

back_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Повернутись до меню \U0001F4F1', callback_data='menu')
    ]
])

confirm_keyboard3 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Так \u2705', callback_data='yes3'),
        InlineKeyboardButton('Ні \u274C', callback_data='no3')
    ],
    [
        InlineKeyboardButton('Повернутись до меню \U0001F4F1', callback_data='menu'),
    ],
])

confirm_keyboard4 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('\u2705', callback_data='yes'),
        InlineKeyboardButton('\u274C', callback_data='no'),
    ]
])

confirm_keyboard5 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Продовжити \u2705', callback_data='continue'),
    ],
    [
        InlineKeyboardButton('Повернутись до меню \U0001F4F1', callback_data='menu'),
    ],
])


select_fish_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Судак', callback_data='Судак'),
        InlineKeyboardButton('Щука', callback_data='Щука'),
        InlineKeyboardButton('Окунь', callback_data='Окунь')
    ],
    [
        InlineKeyboardButton('Сом', callback_data='Сом'),
        InlineKeyboardButton('Короп', callback_data='Короп'),
        InlineKeyboardButton('Товстолоб', callback_data='Товстолоб')
    ],
    [
        InlineKeyboardButton('Карась', callback_data='Карась'),
        InlineKeyboardButton('Плотва', callback_data='Плотва'),
        InlineKeyboardButton('Лящ', callback_data='Лящ')
    ]
])

select_fishcount_keyabord = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('1', callback_data='1'),
        InlineKeyboardButton('2', callback_data='2'),
        InlineKeyboardButton('3', callback_data='3')
    ],
    [
        InlineKeyboardButton('4', callback_data='4'),
        InlineKeyboardButton('5', callback_data='5'),
        InlineKeyboardButton('6', callback_data='6')
    ],
    [
        InlineKeyboardButton('7', callback_data='7'),
        InlineKeyboardButton('8', callback_data='8'),
        InlineKeyboardButton('9', callback_data='9')
    ]
])
