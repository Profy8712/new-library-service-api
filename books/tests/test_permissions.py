import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from books.models import Book

User = get_user_model()


@pytest.mark.django_db
def test_non_admin_cannot_create_book():
    """Non-admin user cannot create books."""
    user = User.objects.create_user(
        email="user@example.com", password="pass1234", is_staff=False
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("book-list")
    data = {
        "title": "NotAllowed",
        "author": "A",
        "cover": "HARD",
        "inventory": 1,
        "daily_fee": 1.0
    }
    response = client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create_book():
    """Admin user can create books."""
    admin = User.objects.create_user(
        email="admin@example.com", password="pass1234", is_staff=True
    )
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("book-list")
    data = {
        "title": "Allowed",
        "author": "Admin",
        "cover": "HARD",
        "inventory": 5,
        "daily_fee": 2.5
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert Book.objects.filter(title="Allowed").exists()
