import threading
import time
from fastapi import FastAPI

from src.database.connection import DB
from src.router import router
from src.routers.card import card_router
from src.routers.transaction import transaction_router
from src.routers.user import user_router
from src.worker.worker import worker

while True:
    db_engine = DB.connect_to_database()
    if db_engine:
        break
    time.sleep(5)

app = FastAPI()

app.include_router(router)
app.include_router(user_router, prefix="/api/v1/user")
app.include_router(card_router, prefix="/api/v1/card")
app.include_router(transaction_router, prefix="/api/v1/transaction")

worker_thread = threading.Thread(target=worker)
worker_thread.daemon = True
worker_thread.start()
