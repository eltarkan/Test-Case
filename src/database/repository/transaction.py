import uuid
from src.database.connection import DB
from src.database.models import Transaction, TransactionTypeEnum, TransactionStatusEnum
from src.database.repository.card import get_user_card_by_card_no


def create_transaction(card_no, user_id, amount, description, type, status):
    session = DB.get_session()()
    try:

        user_card = get_user_card_by_card_no(card_no, user_id)
        if not user_card:
            session.close()
            return {
                "status": "ERROR",
                "message": "Card not found"
            }

        transaction = Transaction(
            uuid=uuid.uuid4(),
            card_id=user_card.id,
            user_id=user_id,
            amount=amount,
            description=description,
            type=TransactionTypeEnum(type),
            status=TransactionStatusEnum(status)
        )
        session.add(transaction)
        session.commit()
        session.close()
        return {
            "status": "OK",
            "transaction": transaction
        }
    except Exception as e:
        session.close()
        print(e)
        return {
            "status": "ERROR",
            "message": str(e)
        }


def get_cards_total_transaction_amount(cards):
    print(cards)

    session = DB.get_session()()
    try:
        total_transaction_amount = 0
        for card in cards:
            transactions = session.query(Transaction).filter(Transaction.card_id == card["id"], Transaction.date_deleted == None, Transaction.status == "SUCCESS").all()
            for transaction in transactions:
                if transaction.type == TransactionTypeEnum.DEPOSIT:
                    total_transaction_amount += transaction.amount
                elif transaction.type == TransactionTypeEnum.WITHDRAW:
                    total_transaction_amount -= transaction.amount
        session.close()
        return total_transaction_amount
    except Exception as e:
        session.close()
        print(e)
        return None


def get_user_transactions(user_id):
    session = DB.get_session()()
    try:
        transactions = session.query(Transaction).filter(Transaction.user_id == user_id, Transaction.date_deleted == None).all()
        session.close()
        return transactions
    except Exception as e:
        session.close()
        print(e)
        return None


def get_transaction_by_uuid(uuid):
    session = DB.get_session()()
    try:
        transaction = session.query(Transaction).filter(Transaction.uuid == uuid, Transaction.date_deleted == None).first()
        session.close()
        return transaction
    except Exception as e:
        session.close()
        print(e)
        return None


def get_total_credit_card_balance(user_id, card_id):
    session = DB.get_session()()
    try:
        total_credit_card_transaction_amount = session.query(Transaction).filter(Transaction.user_id == user_id, Transaction.card_id == card_id, Transaction.date_deleted == None).all()
        session.close()
        total_balance = 0
        for transaction in total_credit_card_transaction_amount:
            if transaction.type == TransactionTypeEnum.DEPOSIT:
                total_balance += transaction.amount
            elif transaction.type == TransactionTypeEnum.WITHDRAW:
                total_balance -= transaction.amount
        return total_balance
    except Exception as e:
        session.close()
        print(e)
        return None


def get_user_successful_transactions(user_id):
    session = DB.get_session()()
    try:
        transactions = session.query(Transaction).filter(Transaction.user_id == user_id, Transaction.status == TransactionStatusEnum.SUCCESS, Transaction.date_deleted == None).all()
        session.close()
        return transactions
    except Exception as e:
        session.close()
        print(e)
        return None
