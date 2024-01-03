from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os


class Database():
    def __init__(self):
        self.engine = None

    def connect_to_database(self):
        try:
            self.engine = create_engine(os.getenv("MYSQL_URL", "mysql://guardian:guardian@mysql:3306/guardian"), echo=True)
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                row = result.fetchone()
                if row[0] == 1:
                    return True
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return False

    def get_session(self):
        return sessionmaker(bind=self.engine)


DB = Database()
