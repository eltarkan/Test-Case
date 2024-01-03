from faker import Faker


def generate_fake_card():
    fake = Faker()
    card_number = fake.credit_card_number(card_type=None)
    return card_number
