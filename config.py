# config.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# File Path
DATA_FILE_PATH = "NEWTEST-inventory-listing-2022-08-17.txt"
