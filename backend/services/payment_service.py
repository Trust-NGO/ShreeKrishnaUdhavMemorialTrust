import os
try:
    import razorpay
except ImportError:
    razorpay = None
from models import Donation
from services.receipt_service import generate_receipt

if razorpay:
    razorpay_client = razorpay.Client(
        auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
)

def verify_payment_and_save(data, db):
    if not razorpay:
        raise ValueError("Razorpay is not installed")

    if not razorpay_client:
        raise ValueError("Razorpay client is not initialized")

    razorpay_client.utility.verify_payment_signature({
        'razorpay_order_id': data['razorpay_order_id'],
        'razorpay_payment_id': data['razorpay_payment_id'],
        'razorpay_signature': data['razorpay_signature']
    })

    donation = Donation(
        donor_name=data['donor_name'],
        donor_email=data['donor_email'],
        amount=data['amount'] / 100,
        transaction_id=data['razorpay_payment_id']
    )

    db.add(donation)
    db.commit()
    db.refresh(donation)

    receipt_id, receipt_url = generate_receipt(donation)

    return {
        "status": "success",
        "receipt": receipt_url
    }