from random import choice
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from keyboards import select_fish_keyboard, select_fishcount_keyabord, confirm_keyboard4
from keyboards import menu_keyboard, confirm_keyboard2, back_menu_keyboard, confirm_keyboard3
from .answers_for_user import ANSWERS
from create_bot import *
from db import *


class CatchFish(StatesGroup):
    have_fishing = State()
    select_fish = State()
    name = State()
    count = State()
    confirm = State()


async def not_have_fishing(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    user_name = callback_query.from_user.first_name
    
    message_for_user = f' Що ж {user_name}, бажаю якнайшвидше знайти час для улюбленного хоббі! 😉'\
                        "Ти обов'язково піймаєш свій трофей! 🐡"
    
    await callback_query.message.answer(message_for_user, reply_markup=back_menu_keyboard)

async def have_fishing_confirm(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(
                        'Підтверди що в тебе сьогодні риболовля 🛳'\
                        'І я занесу дату до твоєї статистики 📈',
                        reply_markup=confirm_keyboard4)
    await state.update_data(user_id = callback_query.from_user.id)
    await CatchFish.have_fishing.set()

async def have_fishing(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    if callback_query.data == 'no':
        await callback_query.message.answer('Повертаюсь до меню 📱, можеш спробувати ще раз ',
                             reply_markup=menu_keyboard)
        await state.finish()
    elif callback_query.data == 'yes':
        data = await state.get_data()
        user_id = data.get('user_id')
        
        async with Session() as session:
            already_fishing = await get_or_create_fishing_trip(session=session, user_id=user_id)
            if already_fishing:
                message_for_user = ANSWERS.get('have_fishing')
            elif not already_fishing:
                message_for_user = ['Що ж, почнемо, ти вже встиг щось зловити? 😊']
        
            await callback_query.message.answer(choice(message_for_user), reply_markup=confirm_keyboard2)
            await CatchFish.select_fish.set()

async def start_catch_fish_dialog(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    if callback_query.data == 'start_dialog':
        await callback_query.message.answer('Круто! Вибери рибу яку ти зловив', 
                         reply_markup=select_fish_keyboard)
        await CatchFish.name.set()
    elif callback_query.data == 'no_catch_fish':
        await callback_query.message.answer('Що ж, певен ти ще встигнеш піймати свій трофей 😌',
                                        reply_markup=back_menu_keyboard)
        await state.finish()
    else:
        await callback_query.message.answer('Вибери розділ 🗂', reply_markup=menu_keyboard)
        await state.finish()
            

async def get_fish_name(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    fish_name = callback_query.data
    await state.update_data(fish_name=fish_name)
    await callback_query.message.answer('Тепер вкажи кількість пійманої риби',
                                        reply_markup=select_fishcount_keyabord)
    await CatchFish.count.set()

async def get_fish_count(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    fish_count = callback_query.data
    await state.update_data(fish_count=fish_count)
    fish_data = await state.get_data()
    fish_name = fish_data.get('fish_name')
    await callback_query.message.answer(f'Отже, твій улов: "{fish_name}" в кількості "{fish_count}". Вірно?',
                                        reply_markup=confirm_keyboard3)
    await CatchFish.confirm.set()

async def handle_confirmation(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    if callback_query.data == "yes3":
        fish_data = await state.get_data()
        fish_name = fish_data.get('fish_name')
        fish_count = int(fish_data.get('fish_count'))
        
        async with Session() as session:
            await create_or_update_fish(session=session, user_id=callback_query.from_user.id, 
                                        fish_name=fish_name, fish_count=fish_count) 
        
        await callback_query.message.answer('Добре, зберігаю дані до твоєї статистики 😉')
        await state.finish()
    elif callback_query.data == "no3":
        await callback_query.message.answer('Добре, спробуємо ще раз, обери назву риби',
                             reply_markup=select_fish_keyboard)
        await CatchFish.name.set()
    elif callback_query.data == 'menu':
        await callback_query.message.answer('Вибери розділ 🗂', reply_markup=menu_keyboard)
        await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(not_have_fishing, lambda c: c.data == 'no_fishing')
    dp.register_callback_query_handler(have_fishing_confirm, lambda c: c.data == 'add_info')
    dp.register_callback_query_handler(start_catch_fish_dialog, state=CatchFish.select_fish)
    dp.register_callback_query_handler(have_fishing, state=CatchFish.have_fishing)
    dp.register_callback_query_handler(get_fish_name, state=CatchFish.name)
    dp.register_callback_query_handler(get_fish_count, state=CatchFish.count)
    dp.register_callback_query_handler(handle_confirmation, state=CatchFish.confirm)