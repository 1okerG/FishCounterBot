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
    ],
    [
        InlineKeyboardButton('Амур', callback_data='Амур'),
        InlineKeyboardButton('Бичок', callback_data='Бичок'),
        InlineKeyboardButton('Лин', callback_data='Лин')
    ],
])

select_fishcount_keyabord = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('\u0031\u20E3', callback_data='1'),
        InlineKeyboardButton('\u0032\u20E3', callback_data='2'),
        InlineKeyboardButton('\u0033\u20E3', callback_data='3')
    ],
    [
        InlineKeyboardButton('\u0034\u20E3', callback_data='4'),
        InlineKeyboardButton('\u0035\u20E3', callback_data='5'),
        InlineKeyboardButton('\u0036\u20E3', callback_data='6')
    ],
    [
        InlineKeyboardButton('\u0037\u20E3', callback_data='7'),
        InlineKeyboardButton('\u0038\u20E3', callback_data='8'),
        InlineKeyboardButton('\u0039\u20E3', callback_data='9')
    ]
])
