from aiogram.utils import executor

from create_bot import *
from handelrs import *



async def on_startup(_):
    pass

menu_handlers.register_handlers(dp)
fishing_process_handlers.register_handlers(dp)
statistics_handlers.register_handlers(dp)
add_past_info_handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)