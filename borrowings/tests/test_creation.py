from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from books.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_borrowing_decrements_inventory():
    user = User.objects.create_user(
        email="borrower@test.com", password="testpass", first_name="B", last_name="U"
    )
    book = Book.objects.create(
        title="DecrementBook", author="A", cover="HARD", inventory=2, daily_fee=1.0
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("borrowing-list")
    data = {
        "book": book.id,
        "expected_return_date": "2030-01-10"
    }
    resp = client.post(url, data)
    assert resp.status_code == 201
    book.refresh_from_db()
    assert book.inventory == 1


@pytest.mark.django_db
def test_cannot_borrow_if_no_inventory():
    user = User.objects.create_user(
        email="borrower2@test.com", password="testpass", first_name="B2", last_name="U2"
    )
    book = Book.objects.create(
        title="OutOfStock", author="A", cover="SOFT", inventory=0, daily_fee=1.0
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("borrowing-list")
    data = {
        "book": book.id,
        "expected_return_date": "2030-02-10"
    }
    resp = client.post(url, data)
    assert resp.status_code == 400
    assert "out of stock" in str(resp.data).lower()
