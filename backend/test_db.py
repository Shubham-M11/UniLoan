import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "uniloan")

url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print("Connecting to:", f"postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")
engine = create_engine(url)
try:
    with engine.connect() as conn:
        print("Success!")
except Exception as e:
    print("Error connecting to DB:", e)
