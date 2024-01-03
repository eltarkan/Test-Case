from faker import Faker


def generate_fake_card():
    fake = Faker()
    card_number = fake.credit_card_number(card_type=None)
    return card_number


# def generate_fake_user():
#     fake = Faker()
#     user = create_user(fake.email(), fake.password())
#     print({
#         "email": user.email,
#         "password": user.password
#     })
#
#
# def generate_fake_users(amount: int = 10):
#     for i in range(amount):
#         generate_fake_user()


# def generate_fake_cards(amount: int = 10, _user=None):
#     for i in range(amount):
#         session = DB.get_session()()
#         _new_card = Card(card_no=generate_fake_card(), status=CardStatusEnum.ACTIVE)
#         session.add(_new_card)
#         session.add(_user)
#         _relation = UserCard()
#         _relation.user = _user
#         _relation.card = _new_card
#         session.add(_relation)
#         session.commit()
