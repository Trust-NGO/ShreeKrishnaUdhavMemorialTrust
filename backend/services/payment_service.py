"""Payment service for Razorpay integration."""

import os
from datetime import datetime

try:
    import razorpay
    from razorpay.exceptions import BadSignatureError
except ImportError:
    razorpay = None
    BadSignatureError = Exception

from fastapi import HTTPException
from models import Donation
from services.receipt_service import generate_receipt
from core.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

if razorpay and RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
else:
    razorpay_client = None


def create_razorpay_order(amount: int):
    """Create a Razorpay order for the given amount (in INR)."""
    if not razorpay:
        raise HTTPException(500, "Payment service unavailable")
    if not razorpay_client:
        raise HTTPException(500, "Payment configuration error")

    order_data = {
        "amount": amount * 100,  # Convert to paise
        "currency": "INR",
        "receipt": f"order_{datetime.now().timestamp()}",
        "payment_capture": 1
    }
    order = razorpay_client.order.create(data=order_data)
    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"]
    }


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
