from sqlalchemy import Column, Integer, Numeric, String, DateTime
from fast_api.database import Base
from datetime import datetime


class Card(Base):
    __tablename__ = "users_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    card_type = Column(String(15), nullable=False)
    card_number = Column(String(19), nullable=False)
    last_four_digit = Column(String(4), nullable=False)
    expiry_data = Column(String(5), nullable=False)
    card_holder_name = Column(String(100), nullable=False)
    balance = Column(Numeric(10,2), nullable=False)


class Transaction(Base):
    __tablename__ = "users_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    card_id = Column(Integer, nullable=False)
    amount = Column(Numeric(5, 2), nullable=False)
    status = Column(String(20), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)