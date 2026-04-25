from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services.payment_service import verify_payment_and_save

router = APIRouter()


@router.post("/verify-payment")
def verify_payment(payment_data: dict, db: Session = Depends(get_db)):
    return verify_payment_and_save(payment_data, db)


@router.post("/test-success")
def test_payment(db: Session = Depends(get_db)):
    from models import Donation
    from services.receipt_service import generate_receipt
    import uuid

    donation = Donation(
        donor_name="Test User",
        donor_email="test@example.com",
        donor_pan ="AHAHAHAHA",
        amount=500,
        transaction_id=f"TEST-{uuid.uuid4().hex[:10]}",

        # ✅ FIXED FIELD NAME
        payment_status="completed"
    )

    db.add(donation)
    db.commit()
    db.refresh(donation)

    receipt_no, receipt_url = generate_receipt(donation, db)

    return {
        "status": "success",
        "receipt_url": receipt_url
    }