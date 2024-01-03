from datetime import datetime

from src.database.connection import DB
from src.database.models import Card, User, UserCard


def create_user_card(user_id: str, card_no: str, label: str):
    try:
        session = DB.get_session()()
        card = session.query(Card).filter(Card.card_no == card_no, Card.date_deleted == None).first()
        if card is None:
            card = Card(card_no=card_no, label=label)
            session.add(card)
            session.commit()
        user_card = UserCard(user_id=user_id, card_id=card.id)
        session.add(user_card)
        session.commit()
        session.close()
        return {
            "status": "OK",
            "card": card
        }
    except Exception as e:
        print(e)
        return {
            "status": "ERROR",
            "message": str(e)
        }


def get_cards_by_user_id(user_id):
    try:
        session = DB.get_session()()
        _user_cards = session.query(UserCard).filter(UserCard.user_id == user_id, UserCard.date_deleted == None).all()
        user_cards = [_user_cards[i] for i in range(len(_user_cards)) if _user_cards[i].card.date_deleted == None]
        session.close()
        return user_cards
    except Exception as e:
        print(e)
        return None


def get_user_card_by_card_no(card_no, user_id):
    session = DB.get_session()()
    try:
        card = session.query(Card).join(Card.users).filter(User.id == user_id, Card.card_no == card_no, Card.date_deleted == None).first()
        session.close()
        return card
    except Exception as e:
        session.close()
        print(e)
        return None


def delete_user_card_with_card_no(card_no, user_id):
    session = DB.get_session()()
    try:
        user_cards = session.query(UserCard).join(UserCard.card).filter(UserCard.user_id == user_id, UserCard.date_deleted == None).all()
        if user_cards is None:
            session.close()
            return {
                "status": "ERROR",
                "message": "Card not found"
            }
        if len(user_cards) == 1:
            session.close()
            return {
                "status": "ERROR",
                "message": "You cannot delete your only card"
            }
        user_card = [user_cards[i] for i in range(len(user_cards)) if user_cards[i].card.card_no == card_no][0]
        user_card.date_deleted = datetime.now()
        session.commit()
        session.close()
        return {
            "status": "OK",
            "card": {}
        }
    except Exception as e:
        session.close()
        return {
            "status": "ERROR",
            "message": str(e)
        }


def activate_credit_card_status(card_no, user_id):
    session = DB.get_session()()
    try:
        user_card = session.query(UserCard).join(UserCard.card).filter(UserCard.user_id == user_id, Card.card_no == card_no, UserCard.date_deleted == None).first()
        if user_card is None:
            session.close()
            return {
                "status": "ERROR",
                "message": "Card not found"
            }
        user_card.card.status = "ACTIVE"
        session.commit()
        session.close()
        return {
            "status": "OK",
            "card": {}
        }
    except Exception as e:
        session.close()
        return {
            "status": "ERROR",
            "message": str(e)
        }


def deactivate_credit_card_status(card_no, user_id):
    session = DB.get_session()()
    try:
        active_user_cards = session.query(UserCard).join(UserCard.card).filter(UserCard.user_id == user_id, Card.status == "ACTIVE", UserCard.date_deleted == None).all()
        print("#" * 10)
        print(active_user_cards)
        print("#" * 10)

        if active_user_cards is None:
            session.close()
            return {
                "status": "ERROR",
                "message": "Card not found"
            }

        if len(active_user_cards) == 1:
            session.close()
            return {
                "status": "ERROR",
                "message": "You cannot deactivate your only card"
            }
        user_card = [active_user_cards[i] for i in range(len(active_user_cards)) if active_user_cards[i].card.card_no == card_no][0]
        user_card.card.status = "PASSIVE"
        session.commit()
        session.close()
        return {
            "status": "OK",
            "card": {}
        }
    except Exception as e:
        session.close()
        return {
            "status": "ERROR",
            "message": str(e)
        }


def get_my_cards_with_label_and_card_no(user_id, card_no, label):
    session = DB.get_session()()
    try:
        filter_user_card = [
            UserCard.user_id == user_id,
            UserCard.date_deleted == None,
        ]
        if label is not None:
            filter_user_card.append(Card.label.like(f"%{label}%"))

        if card_no is not None:
            filter_user_card.append(Card.card_no == card_no)

        user_cards = session.query(UserCard).join(UserCard.card).filter(
            *filter_user_card,
        ).all()

        if user_cards is None:
            session.close()
            return {
                "status": "ERROR",
                "message": "Card not found"
            }

        cards_details = []
        for user_card in user_cards:
            cards_details.append({
                "label": user_card.card.label,
                "card_no": user_card.card.card_no,
                "status": user_card.card.status
            })

        session.close()
        return cards_details
    except Exception as e:
        session.close()
        return {
            "status": "ERROR",
            "message": str(e)
        }


def get_user_active_cards(user_id):
    session = DB.get_session()()
    try:
        user_cards = session.query(UserCard).join(UserCard.card).filter(
            UserCard.user_id == user_id,
            Card.status == "ACTIVE",
            UserCard.date_deleted == None,
        ).all()

        if user_cards is None:
            session.close()
            return {
                "status": "ERROR",
                "message": "Card not found"
            }

        cards_details = []
        for user_card in user_cards:
            cards_details.append({
                "id": user_card.card.id,
                "label": user_card.card.label,
                "card_no": user_card.card.card_no,
                "status": user_card.card.status
            })

        session.close()
        return cards_details
    except Exception as e:
        session.close()
        return {
            "status": "ERROR",
            "message": str(e)
        }


def get_user_passive_cards(user_id):
    session = DB.get_session()()
    try:
        user_cards = session.query(UserCard).join(UserCard.card).filter(
            UserCard.user_id == user_id,
            Card.status == "PASSIVE",
            UserCard.date_deleted == None,
        ).all()

        if user_cards is None:
            session.close()
            return {
                "status": "ERROR",
                "message": "Card not found"
            }

        cards_details = []
        for user_card in user_cards:
            cards_details.append({
                "id": user_card.card.id,
                "label": user_card.card.label,
                "card_no": user_card.card.card_no,
                "status": user_card.card.status
            })

        session.close()
        return cards_details
    except Exception as e:
        session.close()
        return {
            "status": "ERROR",
            "message": str(e)
        }
