import pytest
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from books.models import Book
from borrowings.models import Borrowing

User = get_user_model()

@pytest.mark.django_db
@patch("payments.services.stripe.checkout.Session.create")
def test_create_payment_endpoint(mock_create):
    user = User.objects.create_user(
        email="stripeuser@t.com", password="pw", first_name="S", last_name="U"
    )
    book = Book.objects.create(
        title="SBook", author="B", cover="HARD", inventory=2, daily_fee=8.0
    )
    borrowing = Borrowing.objects.create(
        user=user, book=book, expected_return_date="2040-01-01"
    )

    mock_create.return_value = type("Session", (), {"url": "https://stripe.com/pay", "id": "sess123"})()
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("payment-create")
    resp = client.post(url, {"borrowing_id": borrowing.id, "type": "PAYMENT"})
    assert resp.status_code == 201
    assert resp.data["session_url"] == "https://stripe.com/pay"
    assert resp.data["status"] == "PENDING"

@pytest.mark.django_db
def test_stripe_webhook_marks_payment_paid(client):
    # Create payment
    user = User.objects.create_user(
        email="webhook@t.com", password="pw", first_name="W", last_name="B"
    )
    book = Book.objects.create(
        title="WHBook", author="B", cover="HARD", inventory=2, daily_fee=10.0
    )
    borrowing = Borrowing.objects.create(
        user=user, book=book, expected_return_date="2050-01-01"
    )
    from payments.models import Payment
    payment = Payment.objects.create(
        borrowing=borrowing, status="PENDING", type="PAYMENT",
        session_url="http://stripe.com", session_id="webhook_sess", money_to_pay=99
    )

    from django.test import RequestFactory
    import stripe

    event = {
        "type": "checkout.session.completed",
        "data": {"object": {"id": "webhook_sess"}}
    }
    payload = stripe.webhook.Webhook._encode_event(event)
    rf = RequestFactory()
    # For the test, we skip signature verification.
    request = rf.post("/api/stripe/webhook/", payload, content_type="application/json")
    from payments.webhooks import stripe_webhook_view
    with patch("stripe.Webhook.construct_event") as mock_construct:
        mock_construct.return_value = event
        resp = stripe_webhook_view(request)
    payment.refresh_from_db()
    assert resp.status_code == 200
    assert payment.status == "PAID"
