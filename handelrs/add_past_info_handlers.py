from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from create_bot import *
from db import *
from keyboards import keyboard10, keyboard11, keyboard5, keyboard6, keyboard7, keyboard12, keyboard13


class AddPastInfo(StatesGroup):
    start_dialog = State()
    date_select = State()
    add_date = State()
    fish_set = State()
    fish_get = State()
    fish_count = State()
    fish_confirm = State()

async def start_dialog(message: types.Message):
    await message.answer('''У цьому розділі ти можеш додати дату своїх минулих рибалок 🛳 
А також свої трофеї! 🎣''',
                         reply_markup=keyboard11)
    await AddPastInfo.start_dialog.set()

async def show_calendar(message: types.Message, state: FSMContext):
    if message.text == 'Повернутися до меню 📱':
        await message.answer('Повертаюсь до меню 📱', reply_markup=keyboard7)
        await state.finish()
    elif message.text == 'Продовжити ✅':
        user_id = message.from_user.id
        await state.update_data(user_id=user_id)
        await message.answer('Добре, тепер обери дату риболовлі 📅', 
                            reply_markup=await SimpleCalendar().start_calendar())
        await AddPastInfo.date_select.set()
    else:
        await message.answer('Будь-ласка, скористайся клавіатурою 😐',
                         reply_markup=keyboard11)
        await AddPastInfo.start_dialog.set()

async def select_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        date = date.date()
        if date > datetime.today().date():
            await callback_query.message.answer('Ти обрав дату у майбутньому 😁\nСпробуй ще раз=)',
                                                reply_markup=await SimpleCalendar().start_calendar())
            await AddPastInfo.date_select.set()
        else:
            await state.update_data(date=date)
            await callback_query.message.answer(f'Дата твоєї рибалки: {date}, вірно? 🛳', 
                                                reply_markup=keyboard10)
            await AddPastInfo.add_date.set()

async def add_fishing_date(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'no':
        await callback_query.message.answer('Меню 📱', reply_markup=keyboard7)
        await state.finish()
    else:
        already_fishing = False
        data = await state.get_data()
        user_id = data.get('user_id')
        fishing_date = data.get('date')

        with Session() as session:
            already_fishing = await get_or_create_fishing_trip(session=session, 
                                                               user_id=user_id,
                                                               fishing_date=fishing_date)
        
        if already_fishing:
            message_for_user = 'Бачу, що цього дня ти вже був на риболовлі, хочеш додати трофеї? 😉'
        elif not already_fishing:
            message_for_user = 'Додатю дату до стастистики, ти спіймав тоді рибу? 😉'
        
        await callback_query.message.answer(message_for_user, reply_markup=keyboard12)
        await AddPastInfo.fish_set.set()

async def select_fish_name(message: types.Message, state: FSMContext):
    if message.text == 'Повернутися до меню 📱':
        await message.answer('Повертаюсь до меню 📱', reply_markup=keyboard7)
        await state.finish()
    elif message.text == 'Звісно 😎':
        await message.answer('Круто! Вибери рибу яку ти зловив', 
                            reply_markup=keyboard5)
        await AddPastInfo.fish_get.set()
    else:
        await message.answer('Будь-ласка, скористайся клавіатурою 😐',
                         reply_markup=keyboard12)
        await AddPastInfo.fish_set.set()

async def get_fish_name(callback_query: CallbackQuery, state: FSMContext):
    fish_name = callback_query.data
    await state.update_data(fish_name=fish_name)
    await callback_query.message.answer('Тепер вкажи кількість пійманої риби',
                                        reply_markup=keyboard6)
    await AddPastInfo.fish_count.set()

async def get_fish_count(callback_query: CallbackQuery, state: FSMContext):
    fish_count = callback_query.data
    await state.update_data(fish_count=fish_count)
    data = await state.get_data()
    fish_name = data.get('fish_name')
    await callback_query.message.answer(f'Отже, твій улов: "{fish_name}" в кількості "{fish_count}". Вірно?',
                                        reply_markup=keyboard10)
    await AddPastInfo.fish_confirm.set()

async def confirmation(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "yes":
        data = await state.get_data()
        fish_name = data.get('fish_name')
        fish_count = int(data.get('fish_count'))
        user_id = data.get('user_id')
        fishing_date = data.get('date')
        
        with Session() as session:
            await create_or_update_fish(session=session, user_id=user_id, fishing_date=fishing_date,
                                        fish_name=fish_name, fish_count=fish_count) 
        
        await callback_query.message.answer('Добре, зберігаю дані до твоєї статистики 😉',
                                            reply_markup=keyboard13)
        await state.finish()
    elif callback_query.data == "no":
        await callback_query.message.answer('Повертаюсь до меню 📱, можеш спробувати ще раз ',
                             reply_markup=keyboard7)
        await state.finish()




def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_dialog, text='Додати статистику за минулою датою 🧾')
    dp.register_message_handler(show_calendar, state=AddPastInfo.start_dialog)
    dp.register_callback_query_handler(select_date, simple_cal_callback.filter(), state=AddPastInfo.date_select)
    dp.register_callback_query_handler(add_fishing_date, state=AddPastInfo.add_date)
    dp.register_message_handler(select_fish_name, state=AddPastInfo.fish_set)
    dp.register_callback_query_handler(get_fish_name, state=AddPastInfo.fish_get)
    dp.register_callback_query_handler(get_fish_count, state=AddPastInfo.fish_count)
    dp.register_callback_query_handler(confirmation, state=AddPastInfo.fish_confirm)