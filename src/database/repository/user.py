from src.database.connection import DB
from src.database.faker.generator import generate_fake_card
from src.database.models import User, CardStatusEnum, Card, UserCard
import bcrypt


def get_user_with_email(email: str):
    session = DB.get_session()()
    return session.query(User).filter(User.email == email, User.date_deleted == None).first()


def create_user(email: str, password: str):
    session = DB.get_session()()
    try:
        with session.begin():
            _user = User(email=email, password=bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8'))
            _new_card = Card(card_no=generate_fake_card(), status=CardStatusEnum.ACTIVE)
            session.add(_new_card)
            session.add(_user)
            _relation = UserCard()
            _relation.user = _user
            _relation.card = _new_card
            session.add(_relation)
            session.commit()
            session.close()
        return _user
    except Exception as e:
        session.rollback()
        session.close()
        print(e)
        return e
