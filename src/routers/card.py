from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel

from src.database.repository.card import get_cards_by_user_id, delete_user_card_with_card_no, create_user_card, \
    deactivate_credit_card_status, activate_credit_card_status, get_my_cards_with_label_and_card_no
from src.middlewares import jwt_middleware

card_router = APIRouter()


class DeleteCreditCardRequest(BaseModel):
    card_no: str


class AddCreditCardRequest(BaseModel):
    card_no: str
    label: str


class UpdateCreditCardRequest(BaseModel):
    old_card_no: str
    card_no: str
    label: str


class ActivateCreditCardRequest(BaseModel):
    card_no: str


@card_router.get("/my-cards", dependencies=[Depends(jwt_middleware)])
def get_my_cards(request: Request):
    cards = get_cards_by_user_id(request.state.user.id)
    if cards is None:
        return {"status": "ERROR", "message": "Something went wrong"}
    return {"status": "OK", "cards": cards}


@card_router.post("/delete-card", dependencies=[Depends(jwt_middleware)])
def delete_card(delete_credit_card_request: DeleteCreditCardRequest, request: Request):
    try:
        card = delete_user_card_with_card_no(delete_credit_card_request.card_no, request.state.user.id)
        if card.get("status") == "ERROR":
            return card
        return {"status": "OK", "card": card}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


@card_router.post("/add-card", dependencies=[Depends(jwt_middleware)])
def add_card(add_credit_card_request: AddCreditCardRequest, request: Request):
    try:
        card = create_user_card(request.state.user.id, add_credit_card_request.card_no, add_credit_card_request.label)
        if card.get("status") == "ERROR":
            return card
        return {"status": "OK", "card": card}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


@card_router.post("/update-card", dependencies=[Depends(jwt_middleware)])
def add_card(update_credit_card_request: UpdateCreditCardRequest, request: Request):
    try:
        card = create_user_card(request.state.user.id, update_credit_card_request.card_no, update_credit_card_request.label)
        if card.get("status") == "ERROR":
            return card
        deleted_card = delete_user_card_with_card_no(update_credit_card_request.old_card_no, request.state.user.id)
        if deleted_card.get("status") == "ERROR":
            return {"status": "ERROR", "message": "Delete card failed"}
        return {"status": "OK", "card": card}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


@card_router.post("/activate", dependencies=[Depends(jwt_middleware)])
def activate_card(activate_credit_card_request: ActivateCreditCardRequest, request: Request):
    try:
        card = activate_credit_card_status(activate_credit_card_request.card_no, request.state.user.id)
        if card.get("status") == "ERROR":
            return card
        return {"status": "OK", "card": card}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


@card_router.post("/deactivate", dependencies=[Depends(jwt_middleware)])
def deactivate_card(activate_credit_card_request: ActivateCreditCardRequest, request: Request):
    try:
        card = deactivate_credit_card_status(activate_credit_card_request.card_no, request.state.user.id)
        if card.get("status") == "ERROR":
            return card
        return {"status": "OK", "card": card}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


@card_router.get("/search", dependencies=[Depends(jwt_middleware)])
def search_card(request: Request):
    try:
        card_no = request.query_params.get("card_no")
        label = request.query_params.get("label")
        print("card_no", card_no)
        print("label", label)
        cards = get_my_cards_with_label_and_card_no(request.state.user.id, card_no, label)
        return {"status": "OK", "cards": cards}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
