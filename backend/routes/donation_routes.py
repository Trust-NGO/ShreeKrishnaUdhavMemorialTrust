from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging

from database import get_db
from services.payment_service import verify_payment_and_save
from services.email_service import email_service

logger = logging.getLogger(__name__)
router = APIRouter()

class PaymentVerificationData(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    donor_name: str = None
    donor_email: str = None
    amount: float = None

@router.post("/verify-payment")
def verify_payment(payment_data: PaymentVerificationData, db: Session = Depends(get_db)):
    """Verify payment and save donation record"""
    try:
        if not payment_data.razorpay_order_id or not payment_data.razorpay_payment_id:
            logger.warning("Missing payment information in verification request")
            raise HTTPException(status_code=400, detail="Missing payment information")
        
        result = verify_payment_and_save(payment_data.dict(), db)
        
        # Send donation receipt email if successful
        if result.get("status") == "success" and payment_data.donor_email:
            try:
                subject = "Donation Receipt - Thank You 🙏"
                html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="max-width: 600px; margin: 0 auto;">
                        <h2>Thank You for Your Donation!</h2>
                        <p>Dear {payment_data.donor_name or 'Donor'},</p>
                        <p>We have successfully received your generous donation of <strong>₹{payment_data.amount:,.0f}</strong>.</p>
                        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #28a745;">
                            <p><strong>Receipt:</strong> <a href="{result.get('receipt_url', '#')}" style="color: #0066cc;">Download Your Receipt</a></p>
                        </div>
                        <p>Your contribution is eligible for tax exemption under Section 80G of the Income Tax Act.</p>
                        <p style="margin-top: 30px; color: #666;">
                            Warm regards,<br>
                            <strong>Shri Krishna Udhav Memorial Trust</strong>
                        </p>
                    </div>
                </body>
                </html>
                """
                success, msg = email_service.send_email(payment_data.donor_email, subject, html_content)
                if not success:
                    logger.error(f"Failed to send donation receipt email: {msg}")
            except Exception as e:
                logger.error(f"Email sending error: {str(e)}", exc_info=True)
        
        logger.info(f"Payment verified for {payment_data.donor_email or 'Unknown'}")
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Payment verification error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Payment verification failed")


# Test payment endpoint removed for production safety.
# If test donations are needed, use the Razorpay test mode with key rzp_test_xxx.
