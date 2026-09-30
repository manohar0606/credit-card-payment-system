from fastapi import APIRouter, Depends, HTTPException, status
from fast_api.schemas import paymentrequest
from fast_api.authentication import get_current_user
from sqlalchemy.orm import Session
from fast_api.database import get_db
from fast_api.models import Card, Transaction
from decimal import Decimal

router = APIRouter(
    prefix="/payment",
    tags=["payment"]
)


@router.post("/")
def make_payment(
    payment: paymentrequest,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find the card belonging to the logged-in user
    card = db.query(Card).filter(
        Card.id == payment.card_id,
        Card.user_id == user_id
    ).first()

    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found or does not belong to the user"
        )

    # Validate payment amount
    if payment.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount must be greater than zero"
        )

    # Create transaction initially as PENDING
    transaction = Transaction(
        user_id=user_id,
        card_id=payment.card_id,
        amount=payment.amount,
        status="PENDING"
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Check available balance
    payment_amount = Decimal(str(payment.amount))

    if card.balance < payment_amount:

        transaction.status = "FAILED"

        db.commit()
        db.refresh(transaction)

        return {
            "message": "Transaction Failed",
            "reason": "Insufficient balance",
            "transaction": {
                "id": transaction.id,
                "user_id": transaction.user_id,
                "card_id": transaction.card_id,
                "amount": float(transaction.amount),
                "status": transaction.status,
                "timestamp": transaction.timestamp
            },
            "available_balance": float(card.balance)
        }

    # Payment successful
    card.balance -= payment_amount
    transaction.status = "SUCCESS"

    db.commit()
    db.refresh(transaction)
    db.refresh(card)

    return {
        "message": "Payment successful",
        "transaction": {
            "id": transaction.id,
            "user_id": transaction.user_id,
            "card_id": transaction.card_id,
            "amount": float(transaction.amount),
            "status": transaction.status,
            "timestamp": transaction.timestamp
        },
        "remaining_balance": float(card.balance)
    }