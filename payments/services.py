import stripe
from django.conf import settings
from payments.models import Payment
from borrowings.models import Borrowing

stripe.api_key = settings.STRIPE_API_KEY


class StripeSessionService:
    @staticmethod
    def create_payment_session(borrowing: Borrowing, amount: float, payment_type: str) -> dict:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Library {payment_type.lower()} for: {borrowing.book.title}"
                        },
                        "unit_amount": int(amount * 100),  # cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
        return {
            "session_url": session.url,
            "session_id": session.id,
        }
