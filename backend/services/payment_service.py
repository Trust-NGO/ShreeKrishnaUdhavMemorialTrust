import os
try:
    import razorpay
    from razorpay.exceptions import BadSignatureError
except ImportError:
    razorpay = None
    BadSignatureError = Exception
from fastapi import HTTPException
from models import Donation
from services.receipt_service import generate_receipt

if razorpay:
    razorpay_client = razorpay.Client(
        auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
)

def verify_payment_and_save(data, db):
    if not razorpay:
        raise HTTPException(500, "Payment service unavailable")

    if not razorpay_client:
        raise HTTPException(500, "Payment configuration error")

    try:
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        })
    except BadSignatureError as e:
        raise HTTPException(400, f"Payment signature verification failed: {str(e)}")
    except Exception as e:
        raise HTTPException(500, f"Payment verification error: {str(e)}")

    donation = Donation(
        donor_name=data['donor_name'],
        donor_email=data['donor_email'],
        amount=data['amount'] / 100,
        transaction_id=data['razorpay_payment_id']
    )

    db.add(donation)
    db.commit()
    db.refresh(donation)

    receipt_id, receipt_url = generate_receipt(donation, db)

    return {
        "status": "success",
        "receipt": receipt_url
    }