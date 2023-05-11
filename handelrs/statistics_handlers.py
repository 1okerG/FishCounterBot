from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import date

from create_bot import *
from db import *
from keyboards import keyboard8, keyboard9, keyboard10


class GetStartEndDate(StatesGroup):
    try_month = State()
    show_stats = State()
    


async def try_category(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await bot.send_message(message.from_user.id, 'Обери категорію', reply_markup=keyboard8)

async def per_month_category(callback_query: CallbackQuery, state: FSMContext):
    start_date = date(date.today().year, date.today().month, 1)
    end_date = date.today()
    await state.update_data(start_date=start_date, end_date=end_date)
    await callback_query.message.answer('Підтверди вибір', reply_markup=keyboard10)
    await GetStartEndDate.show_stats.set()
    print(123)

async def per_year_category(callback_query: CallbackQuery, state: FSMContext):
    start_date = date(date.today().year, 1, 1)
    end_date = date.today()
    await state.update_data(start_date=start_date, end_date=end_date)
    await callback_query.message.answer('Підтверди вибір', reply_markup=keyboard10)
    await GetStartEndDate.show_stats.set()

async def by_months_category(callback_query: CallbackQuery):
    await callback_query.message.answer('Обери місяць', reply_markup=keyboard9)
    await GetStartEndDate.try_month.set()

async def by_years_category(message: types.Message):
    await bot.send_message(message.from_user.id,
        'Зараз ця функція знаходиться у розробці, спробуй пізніше, або обери іншу категорію',
        reply_markup=keyboard8)

async def try_month(callback_query: CallbackQuery, state: FSMContext):
    month_number = int(callback_query.data)
    month_date = get_month_range(month_number=month_number)
    await state.update_data(start_date=month_date[0], end_date=month_date[1])
    await callback_query.message.answer('Підтверди вибір', reply_markup=keyboard10)
    await GetStartEndDate.show_stats.set()

async def show_stats(callback_query: CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    user_id = data.get('user_id')
    stats = {}
    
    if start_date > date.today():
        await callback_query.message.answer(
            '''На жаль я не можу зазирнути у майбутнє 😆
Але я певен що на тебе чекають нові круті трофеї 🐡
Спробуй обрати іншу категорію ☺️''', reply_markup=keyboard8
        )
        await state.finish()
    else:
        with Session() as session:
            stats = fishing_statistics(session=session, user_id=user_id, 
                                   start_date=start_date, end_date=end_date)
        await callback_query.message.answer(answers_for_statistics(stats=stats))
        await state.finish()






def register_handlers(dp: Dispatcher):
    dp.register_message_handler(try_category, text='Статистика 📊')
    dp.register_callback_query_handler(per_month_category, lambda c: c.data == 'per_month')
    dp.register_callback_query_handler(per_year_category, lambda c: c.data == 'per_year')
    dp.register_callback_query_handler(by_months_category, lambda c: c.data == 'by_months')
    dp.register_callback_query_handler(by_years_category, lambda c: c.data == 'by_years')
    dp.register_callback_query_handler(try_month, state=GetStartEndDate.try_month)
    dp.register_callback_query_handler(show_stats, state=GetStartEndDate.show_stats)