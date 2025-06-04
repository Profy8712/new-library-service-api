import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from books.models import Book
from borrowings.models import Borrowing
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()

@pytest.mark.django_db
def test_user_can_return_book():
    user = User.objects.create_user(
        email="ret@test.com", password="pass", first_name="R", last_name="U"
    )
    book = Book.objects.create(
        title="Returnable", author="Auth", cover="SOFT", inventory=0, daily_fee=1.5
    )
    borrowing = Borrowing.objects.create(
        user=user, book=book, expected_return_date="2030-10-10", actual_return_date=None
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("borrowing-return-borrowing", args=[borrowing.id])
    resp = client.post(url)
    assert resp.status_code == 200
    borrowing.refresh_from_db()
    book.refresh_from_db()
    assert borrowing.actual_return_date is not None
    assert book.inventory == 1  # inventory increased


@pytest.mark.django_db
def test_cannot_return_twice():
    user = User.objects.create_user(
        email="ret2@test.com", password="pass", first_name="R2", last_name="U2"
    )
    book = Book.objects.create(
        title="ReturnableTwice", author="A", cover="HARD", inventory=0, daily_fee=1.5
    )
    borrowing = Borrowing.objects.create(
        user=user,
        book=book,
        expected_return_date="2031-01-01",
        actual_return_date=date.today()
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("borrowing-return-borrowing", args=[borrowing.id])
    resp = client.post(url)
    assert resp.status_code == 400
    assert "already returned" in str(resp.data).lower()


@pytest.mark.django_db
def test_only_owner_or_admin_can_return():
    user = User.objects.create_user(
        email="own@test.com", password="pass", first_name="O", last_name="N"
    )
    other = User.objects.create_user(
        email="notown@test.com", password="pass", first_name="N", last_name="O"
    )
    admin = User.objects.create_superuser(
        email="ad@test.com", password="pass", first_name="A", last_name="D"
    )
    book = Book.objects.create(
        title="AccessBook", author="Auth", cover="SOFT", inventory=0, daily_fee=1.5
    )
    borrowing = Borrowing.objects.create(
        user=user, book=book, expected_return_date="2031-10-10", actual_return_date=None
    )

    url = reverse("borrowing-return-borrowing", args=[borrowing.id])

    # Owner can
    client = APIClient()
    client.force_authenticate(user=user)
    resp = client.post(url)
    assert resp.status_code == 200

    # Admin can
    borrowing.actual_return_date = None
    borrowing.save()
    book.inventory = 0
    book.save()
    client.force_authenticate(user=admin)
    resp = client.post(url)
    assert resp.status_code == 200

    # Not owner - forbidden
    borrowing.actual_return_date = None
    borrowing.save()
    book.inventory = 0
    book.save()
    client.force_authenticate(user=other)
    resp = client.post(url)
    assert resp.status_code in (403, 404)
