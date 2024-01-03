import time

from src.database.models import TransactionTypeEnum, TransactionStatusEnum
from src.database.repository.card import get_user_card_by_card_no
from src.database.repository.transaction import create_transaction, get_total_credit_card_balance
from src.queue.queue import TransactionQueue


def worker():
    print('Worker is running... 🚀')
    while True:
        print("Checking queue...")
        data = TransactionQueue.pop()
        if data is not None:
            print("Processing queue...")
            status = TransactionStatusEnum.SUCCESS
            card = get_user_card_by_card_no(data["card_no"], data["user_id"])
            if card is None:
                print("Card not found")
                continue

            balance = get_total_credit_card_balance(data["user_id"], card.id)
            if data["type"] == "WITHDRAW" and balance < data["transaction_amount"]:
                status = TransactionStatusEnum.FAIL
                print("Insufficient balance")
            response = create_transaction(data["card_no"], data["user_id"], data["transaction_amount"], data["description"], data["type"], status)
            print(response)
        time.sleep(5)
