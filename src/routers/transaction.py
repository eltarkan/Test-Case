from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel

from src.database.models import TransactionTypeEnum, TransactionStatusEnum
from src.database.repository.card import get_user_card_by_card_no, get_user_active_cards, get_user_passive_cards
from src.database.repository.transaction import create_transaction, get_total_credit_card_balance, \
    get_user_transactions, get_user_successful_transactions, get_cards_total_transaction_amount
from src.middlewares import jwt_middleware
from src.queue.queue import TransactionQueue

transaction_router = APIRouter()


class CreateTransactionRequest(BaseModel):
    card_no: str
    amount: float
    description: str
    type: str


@transaction_router.post("/process", dependencies=[Depends(jwt_middleware)])
def deposit(request: Request, body: CreateTransactionRequest):
    try:
        data = {
                "user_id": request.state.user.id,
                "transaction_amount": body.amount,
                "card_no": body.card_no,
                "description": body.description,
                "type": body.type
            }
        # create_transaction(data["card_no"], data["user_id"], data["transaction_amount"], data["description"], data["type"])
        TransactionQueue.push(
            data
        )

        return {
            "status": "OK"
        }
    except Exception as e:
        print(e)
        return {
            "status": "ERROR",
            "message": str(e)
        }


@transaction_router.get("/me", dependencies=[Depends(jwt_middleware)])
def me(request: Request):
    try:
        active_cards = get_user_active_cards(request.state.user.id)
        passive_cards = get_user_passive_cards(request.state.user.id)
        active_cards_balance = get_cards_total_transaction_amount(active_cards)
        passive_cards_balance = get_cards_total_transaction_amount(passive_cards)
        return {
            "status": "OK",
            "total_active_cards": len(active_cards),
            "active_cards_balance": active_cards_balance,
            "total_passive_cards": len(passive_cards),
            "passive_cards_balance": passive_cards_balance,
        }
    except Exception as e:
        print(e)
        return {
            "status": "ERROR",
            "message": str(e)
        }
