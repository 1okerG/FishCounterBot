from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup

keyboard1 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='/start'),
                KeyboardButton(text='/help')
            ]
        ],
        resize_keyboard=True
    )

keyboard2 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Так!😎'),
                KeyboardButton(text='Ні 😢'),
            ],
            [
                KeyboardButton(text='Меню 📱'),
            ]
        ],
        resize_keyboard=True
    )

keyboard3 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Авжеш! 😎'),
                KeyboardButton(text='Я завершив рибалку 😑'),
            ],
            [
                KeyboardButton(text='Меню 📱')
            ]
        ],
        resize_keyboard=True
    )

keyboard4 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Так"),
                KeyboardButton(text="Ні"),
            ],
            [
                KeyboardButton(text='Меню 📱')
            ]
        ],
        resize_keyboard=True
    )

keyboard7 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Я починаю / продовжую риболовлю 😎'),
            ],
            [
                KeyboardButton(text='Статистика 📊'),
                KeyboardButton(text='FAQ ☎️'),
            ]
        ],
        resize_keyboard=True
    )


keyboard5 = InlineKeyboardMarkup(inline_keyboard=[
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


keyboard6 = InlineKeyboardMarkup(inline_keyboard=[
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

keyboard8 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('За цей місяць \U0001F4C8', callback_data='per_month'),
        InlineKeyboardButton('Обрати місяць \U0001F4D2', callback_data='by_months'),
    ],
    [
        InlineKeyboardButton('За цей рік \U0001F4C9', callback_data='per_year'),
        InlineKeyboardButton('Обрати рік \U0001F4C6', callback_data='by_years'),
    ],
])

keyboard9 = InlineKeyboardMarkup(inline_keyboard=[
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

keyboard10 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('\u2705', callback_data='yes'),
        InlineKeyboardButton('\u274C', callback_data='no'),
    ]
])