from aiogram.utils import executor

from create_bot import *
from handelrs import fishing_process_handlers, menu_handlers, statistics_handlers



async def on_startup(_):
    pass

menu_handlers.register_handlers(dp)
fishing_process_handlers.register_handlers(dp)
statistics_handlers.register_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup, timeout=60)