from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch values from .env
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False")  # default to False 

# debug
print(f"Loaded DATABASE_URL: {DATABASE_URL}")
print(f"Loaded SECRET_KEY: {SECRET_KEY}")
print(f"Loaded DEBUG Mode: {DEBUG}")
