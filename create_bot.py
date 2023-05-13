from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from config import TOKEN, DATABASE_URL
from db import create_engine, get_session_maker

# load_dotenv()

# TOKEN = os.getenv('TOKEN')

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async_engine = create_engine(DATABASE_URL)
Session = get_session_maker(async_engine)

