from datetime import datetime, date
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from create_bot import *
from db import *
from keyboards import confirm_keyboard3, confirm_keyboard4, confirm_keyboard5, menu_keyboard
from keyboards import select_fish_keyboard, select_fishcount_keyabord, back_menu_keyboard


class AddPastInfo(StatesGroup):
    start_dialog = State()
    date_select = State()
    add_date = State()
    fish_set = State()
    fish_get = State()
    fish_count = State()
    fish_confirm = State()

async def start_dialog(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer('''У цьому розділі ти можеш додати дату своїх минулих рибалок 🛳 
А також свої трофеї! 🎣''',
                         reply_markup=confirm_keyboard5)
    await AddPastInfo.start_dialog.set()

async def show_calendar(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    if callback_query.data == 'menu':
        await callback_query.message.answer('Повертаюсь до меню 📱', reply_markup=menu_keyboard)
        await state.finish()
    elif callback_query.data == 'continue':
        await callback_query.message.answer('Добре, тепер обери дату риболовлі 📅', 
                            reply_markup=await SimpleCalendar().start_calendar())
        await AddPastInfo.date_select.set()

async def select_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, fishing_date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        fishing_date = fishing_date.date()
        if fishing_date > datetime.date.today():
            await callback_query.message.answer('Ти обрав дату у майбутньому 😁\nСпробуй ще раз=)',
                                                reply_markup=await SimpleCalendar().start_calendar())
            await AddPastInfo.date_select.set()
        else:
            await state.update_data(date=fishing_date)
            await callback_query.message.answer(f'Дата твоєї рибалки: {fishing_date}, вірно? 🛳', 
                                                reply_markup=confirm_keyboard4)
            await AddPastInfo.add_date.set()

async def add_fishing_date(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    if callback_query.data == 'no':
        await callback_query.message.answer('Меню 📱', reply_markup=menu_keyboard)
        await state.finish()
    else:
        already_fishing = False
        data = await state.get_data()
        user_id = callback_query.from_user.id
        fishing_date = data.get('date')

        async with Session() as session:
            already_fishing = await get_or_create_fishing_trip(session=session, 
                                                               user_id=user_id,
                                                               fishing_date=fishing_date)
        
        if already_fishing:
            message_for_user = 'Бачу, що цього дня ти вже був на риболовлі, хочеш додати трофеї? 😉'
        elif not already_fishing:
            message_for_user = 'Додаю дату до стастистики, ти спіймав тоді рибу? 😉'
        
        await callback_query.message.answer(message_for_user, reply_markup=confirm_keyboard3)
        await AddPastInfo.fish_set.set()

async def select_fish_name(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    if callback_query.data == 'yes3':
        await callback_query.message.answer('Круто! Вибери рибу яку ти зловив', 
                         reply_markup=select_fish_keyboard)
        await AddPastInfo.fish_get.set()
    elif callback_query.data == 'no3':
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
    await AddPastInfo.fish_count.set()

async def get_fish_count(callback_query: CallbackQuery, state: FSMContext):
    fish_count = callback_query.data
    await state.update_data(fish_count=fish_count)
    data = await state.get_data()
    fish_name = data.get('fish_name')
    await callback_query.message.answer(f'Отже, твій улов: "{fish_name}" в кількості "{fish_count}". Вірно?',
                                        reply_markup=confirm_keyboard4)
    await AddPastInfo.fish_confirm.set()

async def confirmation(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "yes":
        data = await state.get_data()
        fish_name = data.get('fish_name')
        fish_count = int(data.get('fish_count'))
        user_id = callback_query.from_user.id
        fishing_date = data.get('date')
        
        async with Session() as session:
            await create_or_update_fish(session=session, user_id=user_id, fishing_date=fishing_date,
                                        fish_name=fish_name, fish_count=fish_count) 
        
        await callback_query.message.answer('Добре, зберігаю дані до твоєї статистики 😉',
                                            reply_markup=back_menu_keyboard)
        await state.finish()
    elif callback_query.data == "no":
        await callback_query.message.answer('Повертаюсь до меню 📱, можеш спробувати ще раз ',
                             reply_markup=menu_keyboard)
        await state.finish()




def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_dialog, lambda c: c.data == 'add_past_info')
    dp.register_callback_query_handler(show_calendar, state=AddPastInfo.start_dialog)
    dp.register_callback_query_handler(select_date, simple_cal_callback.filter(), state=AddPastInfo.date_select)
    dp.register_callback_query_handler(add_fishing_date, state=AddPastInfo.add_date)
    dp.register_callback_query_handler(select_fish_name, state=AddPastInfo.fish_set)
    dp.register_callback_query_handler(get_fish_name, state=AddPastInfo.fish_get)
    dp.register_callback_query_handler(get_fish_count, state=AddPastInfo.fish_count)
    dp.register_callback_query_handler(confirmation, state=AddPastInfo.fish_confirm)