import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from books.models import Book
from borrowings.models import Borrowing
from payments.models import Payment

User = get_user_model()

@pytest.mark.django_db
def test_user_sees_only_own_payments():
    user1 = User.objects.create_user(
        email="u1@t.com", password="pw", first_name="U1", last_name="T"
    )
    user2 = User.objects.create_user(
        email="u2@t.com", password="pw", first_name="U2", last_name="T"
    )
    book = Book.objects.create(
        title="PaidBook", author="A", cover="HARD", inventory=2, daily_fee=5.0
    )
    borrowing1 = Borrowing.objects.create(
        user=user1, book=book, expected_return_date="2031-01-01"
    )
    borrowing2 = Borrowing.objects.create(
        user=user2, book=book, expected_return_date="2031-02-01"
    )
    pay1 = Payment.objects.create(
        borrowing=borrowing1, status="PENDING", type="PAYMENT",
        session_url="http://url1", session_id="sess1", money_to_pay=15
    )
    pay2 = Payment.objects.create(
        borrowing=borrowing2, status="PENDING", type="PAYMENT",
        session_url="http://url2", session_id="sess2", money_to_pay=10
    )
    client = APIClient()
    client.force_authenticate(user=user1)
    url = reverse("payment-list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert resp.data[0]["id"] == pay1.id

@pytest.mark.django_db
def test_admin_sees_all_payments():
    admin = User.objects.create_superuser(
        email="admin@t.com", password="pw", first_name="A", last_name="D"
    )
    book = Book.objects.create(
        title="B", author="A", cover="SOFT", inventory=1, daily_fee=3.0
    )
    user = User.objects.create_user(
        email="u3@t.com", password="pw", first_name="U3", last_name="T"
    )
    borrowing = Borrowing.objects.create(
        user=user, book=book, expected_return_date="2035-01-01"
    )
    Payment.objects.create(
        borrowing=borrowing, status="PAID", type="PAYMENT",
        session_url="http://url", session_id="sess", money_to_pay=99
    )
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("payment-list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert len(resp.data) >= 1
