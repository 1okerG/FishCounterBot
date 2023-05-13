from random import choice
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from keyboards import keyboard3, keyboard4, keyboard5, keyboard6, keyboard7, keyboard10
from create_bot import *
from db import *


class CatchFish(StatesGroup):
    have_fishing = State()
    select_fish = State()
    name = State()
    count = State()
    confirm = State()


async def not_have_fishing(message: types.Message):
    user_name = message.chat.first_name
    
    message_for_user = f''' Що ж {user_name}, бажаю якнайшвидше знайти час для улюбленного хоббі! 😉
Ти обов'язково піймаєш свій трофей! 🐡
        '''
    
    await bot.send_message(message.from_user.id, message_for_user, reply_markup=keyboard7)

async def have_fishing_confirm(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 
                           'Підтверди що в тебе сьогодні риболовля і я занесу дату до статистики 📈',
                           reply_markup=keyboard10)
    await state.update_data(user_id = message.from_user.id)
    await CatchFish.have_fishing.set()

async def have_fishing(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'no':
        await callback_query.message.answer('Повертаюсь до меню 📱, можеш спробувати ще раз ',
                             reply_markup=keyboard7)
        await state.finish()
    else:
        data = await state.get_data()
        user_id = data.get('user_id')
        print(type(user_id), user_id, sep='\n\n', end='\n\n\n\n')
        
        async with Session() as session:
            already_fishing = await get_or_create_fishing_trip(session=session, user_id=user_id)
            if already_fishing:
                message_for_user = [
                    'Схоже ти вже на риболовлі, ти зловив ще трофеї? 😉',
                    'Я бачу ти продовжуєш рибалити, як успіхи, впіймав ще? 😉',
                    'Так-так-так, новий трофей? 😉',
                    'Риболовля триває, а чи є нові трофеї? 😉'
                                    ]
            elif not already_fishing:
                message_for_user = ['Що ж, почнемо, ти вже встиг щось зловити? 😊']
        
            await callback_query.message.answer(choice(message_for_user), reply_markup=keyboard3)
            await CatchFish.select_fish.set()


async def start_catch_fish_dialog(message: types.Message):
    await message.answer('Круто! Вибери рибу яку ти зловив', 
                         reply_markup=keyboard5)
    await CatchFish.name.set()

async def get_fish_name(callback_query: CallbackQuery, state: FSMContext):
    fish_name = callback_query.data
    await state.update_data(fish_name=fish_name)
    await callback_query.message.answer('Тепер вкажи кількість пійманої риби',
                                        reply_markup=keyboard6)
    await CatchFish.count.set()

async def get_fish_count(callback_query: CallbackQuery, state: FSMContext):
    fish_count = callback_query.data
    await state.update_data(fish_count=fish_count)
    fish_data = await state.get_data()
    fish_name = fish_data.get('fish_name')
    await callback_query.message.answer(f'Отже, твій улов: "{fish_name}" в кількості "{fish_count}". Вірно?',
                                        reply_markup=keyboard4)
    await CatchFish.confirm.set()

async def handle_confirmation(message: types.Message, state: FSMContext):
    if message.text == "Так":
        fish_data = await state.get_data()
        fish_name = fish_data.get('fish_name')
        fish_count = int(fish_data.get('fish_count'))
        
        async with Session() as session:
            await create_or_update_fish(session=session, user_id=message.from_user.id, 
                                        fish_name=fish_name, fish_count=fish_count) 
        
        await message.answer('Добре, зберігаю дані до твоєї статистики 😉')
        await state.finish()
    elif message.text == "Ні":
        await message.answer('Добре, спробуємо ще раз, обери назву риби',
                             reply_markup=keyboard5)
        await CatchFish.name.set()
    elif message.text == 'Меню 📱':
        await message.answer('Вибери дію', reply_markup=keyboard7)
        await state.finish()
    else:
        await message.answer('Будь-ласка, обери "Так" або "Ні"')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(not_have_fishing, text='Ні 😢')
    dp.register_message_handler(have_fishing_confirm, text='Так!😎') 
    dp.register_message_handler(have_fishing_confirm, text='Я починаю|продовжую риболовлю 😎') 
    dp.register_message_handler(start_catch_fish_dialog, text='Авжеш! 😎', state=CatchFish.select_fish)
    dp.register_callback_query_handler(have_fishing, state=CatchFish.have_fishing)
    dp.register_callback_query_handler(get_fish_name, state=CatchFish.name)
    dp.register_callback_query_handler(get_fish_count, state=CatchFish.count)
    dp.register_message_handler(handle_confirmation, state=CatchFish.confirm)