from sqlalchemy import create_engine
from sqlalchemy.sql import text
from fastapi import FastAPI
import os
import time

from src.router import router

app = FastAPI()

app.include_router(router)


def connect_to_database():
    try:
        engine = create_engine(os.getenv("MYSQL_URL", "mysql://guardian:guardian@mysql:3306/guardian"), echo=True)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            if row[0] == 1:
                return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


while True:
    db_engine = connect_to_database()
    if db_engine:
        break
    time.sleep(5)
