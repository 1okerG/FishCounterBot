from dotenv import load_dotenv
import os

load_dotenv()


TOKEN = os.environ.get("TOKEN")

DATABASE_URL = os.environ.get("DATABASE_URL")