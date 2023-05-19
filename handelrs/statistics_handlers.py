from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import date

from create_bot import *
from db import *
from .answers_for_user import ANSWERS
from keyboards import stats_category_keyboard, month_keyboard, confirm_keyboard4, back_menu_keyboard


class GetStartEndDate(StatesGroup):
    try_month = State()
    show_stats = State()
    


async def try_category(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await state.update_data(user_id=callback_query.from_user.id)
    await callback_query.message.answer('Обери категорію 📁', reply_markup=stats_category_keyboard)

async def per_month_category(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    start_date = date(date.today().year, date.today().month, 1)
    end_date = date.today()
    await state.update_data(start_date=start_date, end_date=end_date)
    await callback_query.message.answer('Підтверди вибір', reply_markup=confirm_keyboard4)
    await GetStartEndDate.show_stats.set()
    print(123)

async def per_year_category(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    start_date = date(date.today().year, 1, 1)
    end_date = date.today()
    await state.update_data(start_date=start_date, end_date=end_date)
    await callback_query.message.answer('Підтверди вибір', reply_markup=confirm_keyboard4)
    await GetStartEndDate.show_stats.set()

async def by_months_category(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer('Обери місяць', reply_markup=month_keyboard)
    await GetStartEndDate.try_month.set()

async def by_years_category(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(
        'Зараз ця функція знаходиться у розробці, спробуй пізніше, або обери іншу категорію',
        reply_markup=stats_category_keyboard)

async def try_month(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    month_number = int(callback_query.data)
    month_date = await get_month_range(month_number=month_number)
    await state.update_data(start_date=month_date[0], end_date=month_date[1])
    await callback_query.message.answer('Підтверди вибір', reply_markup=confirm_keyboard4)
    await GetStartEndDate.show_stats.set()

async def show_stats(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    
    data = await state.get_data()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    user_id = data.get('user_id')
    stats = {}
    
    if start_date > date.today():
        await callback_query.message.answer(ANSWERS.get('show_stats'), 
                                            reply_markup=stats_category_keyboard)
        await state.finish()
    else:
        async with Session() as session:
            stats = await fishing_statistics(session=session, user_id=user_id, 
                                   start_date=start_date, end_date=end_date)
        await callback_query.message.answer(await answers_for_statistics(stats=stats), 
                                            reply_markup=back_menu_keyboard)
        await state.finish()






def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(try_category, lambda c: c.data == 'stats')
    dp.register_callback_query_handler(per_month_category, lambda c: c.data == 'per_month')
    dp.register_callback_query_handler(per_year_category, lambda c: c.data == 'per_year')
    dp.register_callback_query_handler(by_months_category, lambda c: c.data == 'by_months')
    dp.register_callback_query_handler(by_years_category, lambda c: c.data == 'by_years')
    dp.register_callback_query_handler(try_month, state=GetStartEndDate.try_month)
    dp.register_callback_query_handler(show_stats, state=GetStartEndDate.show_stats)