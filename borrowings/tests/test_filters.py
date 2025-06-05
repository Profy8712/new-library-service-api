from rest_framework.test import APIClient
import pytest
from django.urls import reverse

from books.models import Book
from borrowings.models import Borrowing
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

@pytest.fixture
def setup_borrowings(db):
    user1 = User.objects.create_user(
        email="user1@test.com", password="p1", first_name="U1", last_name="U1"
    )
    user2 = User.objects.create_user(
        email="user2@test.com", password="p2", first_name="U2", last_name="U2"
    )
    book = Book.objects.create(
        title="FBook", author="F", cover="SOFT", inventory=5, daily_fee=2.5
    )
    b1 = Borrowing.objects.create(
        user=user1,
        book=book,
        expected_return_date="2030-01-01",
        actual_return_date=None
    )
    b2 = Borrowing.objects.create(
        user=user1,
        book=book,
        expected_return_date="2030-02-01",
        actual_return_date=date.today()
    )
    b3 = Borrowing.objects.create(
        user=user2,
        book=book,
        expected_return_date="2030-03-01",
        actual_return_date=None
    )
    return user1, user2, [b1, b2, b3]


@pytest.mark.django_db
def test_is_active_filter_returns_only_active(setup_borrowings):
    user1, user2, borrowings = setup_borrowings
    client = APIClient()
    client.force_authenticate(user=user1)
    url = reverse("borrowing-list")
    resp = client.get(url, {"is_active": True})
    assert resp.status_code == 200
    # user1 only, only active
    assert len(resp.data) == 1
    assert resp.data[0]["actual_return_date"] is None

    resp = client.get(url, {"is_active": False})
    assert len(resp.data) == 1
    assert resp.data[0]["actual_return_date"] is not None


@pytest.mark.django_db
def test_admin_can_filter_by_user(setup_borrowings):
    user1, user2, borrowings = setup_borrowings
    admin = User.objects.create_superuser(
        email="admin@t.com", password="admintest", first_name="A", last_name="D"
    )
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("borrowing-list")
    resp = client.get(url, {"user": user2.id})
    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert resp.data[0]["user"] == user2.email
