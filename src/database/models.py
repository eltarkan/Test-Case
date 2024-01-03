from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func
from enum import Enum as PythonEnum

Base = declarative_base()


class CardStatusEnum(PythonEnum):
    PASSIVE = "PASSIVE"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"


class TransactionStatusEnum(PythonEnum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    PENDING = "PENDING"


class TransactionTypeEnum(PythonEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime(), nullable=False, default=func.now())
    date_modified = Column(DateTime(), nullable=False, default=func.now(), onupdate=func.now())
    date_deleted = Column(DateTime(), nullable=True, default=None)


# card_user_m2m_relation = Table(
#     'card_user_m2m_relation',
#     Base.metadata,
#     Column('card_id', Integer, ForeignKey('card.id')),
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('date_deleted', DateTime(), nullable=True, default=None)
# )


class User(BaseModel):
    __tablename__ = "users"
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)


class Card(BaseModel):
    __tablename__ = "card"  # why is this not cards? That's not my fault, it's from quiz.
    label = Column(String(100), nullable=True)
    card_no = Column(String(24), unique=True, index=True, nullable=False)
    status = Column(Enum(CardStatusEnum), nullable=False, default=CardStatusEnum.PASSIVE)


class UserCard(BaseModel):
    __tablename__ = "user_card"
    user_id = Column(Integer, ForeignKey('users.id'))
    card_id = Column(Integer, ForeignKey('card.id'))
    card = relationship("Card", backref="users")
    user = relationship("User", backref="cards")


class Transaction(BaseModel):
    __tablename__ = "transactions"
    uuid = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    card_id = Column(Integer, ForeignKey('card.id'))
    amount = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Enum(TransactionStatusEnum), nullable=False, default=TransactionStatusEnum.PENDING)
    type = Column(Enum(TransactionTypeEnum), nullable=False, default=TransactionTypeEnum.DEPOSIT)
    card = relationship("Card", backref="transaction_users")
    user = relationship("User", backref="transaction_cards")
