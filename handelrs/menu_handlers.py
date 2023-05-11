from aiogram import types

from create_bot import *
from keyboards import keyboard7, keyboard2
from db import *


async def start(message: types.Message):
    with Session() as session:
        user_id = message.from_user.id
        user_name = message.chat.first_name
        user = await get_or_create_user(session, user_id=user_id, user_name=user_name)
        
        message_for_user = f'''Привіт {user.user_name}! 🙋
Я допоможу тобі вести статистику твоїх рибалок. 
Ты вже розпочав риболовлю? 🎣'''
        
    await bot.send_message(message.from_user.id, message_for_user, reply_markup=keyboard2)

async def menu(message: types.Message):
    await message.answer('Вибери розділ 🗂', reply_markup=keyboard7)

async def help_info(message: types.Message):
    message_for_user = f'''Привіт {message.chat.first_name}, ласкаво просимо в FishCountBot,
що допоможе зберігати та відстежувати статистику твоєї риболовлі! 😎

З нашим ботом ти можеш легко вести облік своїх уловів - зберігати кількість риб, їх назви та дату риболовлі. 🎣
Це дозволить тобі не лише не забувати, скільки і яку рибу ти піймав, але й аналізувати свої улови, 
виявляти закономірності та планувати майбутні риболовлі. 🐟

Крім того, наш бот дозволяє переглядати збережену статистику за обраним періодом часу. 📊
Ти зможеш побачити, яка риба була піймана в певний період, 
скільки загалом риби було піймано та багато іншого. 🌅

Не пропусти можливість контролювати свої риболовні досягнення та зробити свої майбутні риболовлі більш продуктивними та цікавими. 
Спробуй наш бот уже сьогодні та насолоджуйся своїми уловами! 💯👍'''

    await message.answer(message_for_user)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(menu, text='Меню 📱')
    dp.register_message_handler(menu, text='Я завершив рибалку 😑')
    dp.register_message_handler(menu, text='Повернутися до меню 📱')
    dp.register_message_handler(help_info, text='FAQ ☎️')