import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from books.models import Book
from borrowings.models import Borrowing

User = get_user_model()


@pytest.fixture
def book(db):
    return Book.objects.create(
        title="TestBook",
        author="Author",
        cover="HARD",
        inventory=3,
        daily_fee=2.0
    )


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@test.com",
        password="testpass123",
        first_name="Test",
        last_name="User"
    )


@pytest.fixture
def admin(db):
    return User.objects.create_superuser(
        email="admin@test.com",
        password="adminpass123",
        first_name="Admin",
        last_name="User"
    )


@pytest.mark.django_db
def test_user_sees_only_own_borrowings(user, book):
    client = APIClient()
    other_user = User.objects.create_user(
        email="other@test.com",
        password="pass",
        first_name="Other",
        last_name="User"
    )
    Borrowing.objects.create(user=user, book=book, expected_return_date="2030-01-01")
    Borrowing.objects.create(user=other_user, book=book, expected_return_date="2030-01-02")

    client.force_authenticate(user=user)
    url = reverse("borrowing-list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert resp.data[0]["user"] == user.email


@pytest.mark.django_db
def test_admin_sees_all_borrowings(admin, user, book):
    client = APIClient()
    Borrowing.objects.create(user=user, book=book, expected_return_date="2030-01-01")
    Borrowing.objects.create(user=admin, book=book, expected_return_date="2030-01-02")

    client.force_authenticate(user=admin)
    url = reverse("borrowing-list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert len(resp.data) == 2


@pytest.mark.django_db
def test_unauthenticated_cannot_list_borrowings():
    client = APIClient()
    url = reverse("borrowing-list")
    resp = client.get(url)
    assert resp.status_code == 401
