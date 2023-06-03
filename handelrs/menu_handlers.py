from aiogram import types
from aiogram.types import CallbackQuery

from create_bot import *
from keyboards import menu_keyboard, confirm_keyboard1, back_menu_keyboard, callback_keyboard
from db import *
from .answers_for_user import ANSWERS


async def start(message: types.Message):
    async with Session() as session:
        user_id = message.from_user.id
        user_name = message.chat.first_name
        user = await get_or_create_user(session, user_id=user_id, user_name=user_name)
        
        message_for_user = f'''Привіт {user.user_name}! 🙋
Я допоможу тобі вести статистику твоїх рибалок. 
Ты вже розпочав риболовлю? 🎣'''
        
    await message.answer(message_for_user, reply_markup=confirm_keyboard1)

async def menu(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer('Вибери розділ 🗂', reply_markup=menu_keyboard)

async def help_info(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(ANSWERS.get('help_info'), reply_markup=back_menu_keyboard)

async def callback_category(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer("Обери форму зворотнього зв'язку 📮", 
                                        reply_markup=callback_keyboard)

async def bag_report(callback_query: CallbackQuery):
    pass

# async def backup_handler(message: types.Message):
#     backup_postgresql_db(database_uri=DATABASE_URL)
        


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    # dp.register_message_handler(backup_handler, text='/backup')
    dp.register_callback_query_handler(help_info, lambda c: c.data == 'faq')
    dp.register_callback_query_handler(menu, lambda c: c.data == 'menu')
    dp.register_callback_query_handler(callback_category, lambda c: c.data == 'callback')