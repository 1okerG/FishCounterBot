from dotenv import load_dotenv
import os

load_dotenv()


TOKEN = os.environ.get("TOKEN")

DATABASE_URL = 'postgresql+asyncpg://inquisitor:741852963b@localhost:5432/fish_info'