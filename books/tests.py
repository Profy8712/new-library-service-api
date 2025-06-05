from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
import pytest
from django.core.exceptions import ValidationError
from books.models import Book


@pytest.mark.django_db
def test_book_creation():
    """Test creating a Book instance."""
    book = Book.objects.create(
        title="Test Book",
        author="John Doe",
        cover=Book.CoverType.HARD,
        inventory=5,
        daily_fee=2.50
    )
    assert book.id is not None
    assert book.title == "Test Book"
    assert book.cover == "HARD"


@pytest.mark.django_db
def test_book_inventory_validation():
    """Test Book inventory cannot be negative."""
    with pytest.raises(ValidationError):
        book = Book(
            title="Negative Inventory",
            author="Jane Smith",
            cover=Book.CoverType.SOFT,
            inventory=-2,
            daily_fee=1.50
        )
        book.full_clean()


@pytest.mark.django_db
def test_book_daily_fee_validation():
    """Test Book daily_fee cannot be negative."""
    with pytest.raises(ValidationError):
        book = Book(
            title="Negative Fee",
            author="Jane Smith",
            cover=Book.CoverType.HARD,
            inventory=2,
            daily_fee=-5.00
        )
        book.full_clean()

@pytest.mark.django_db
def test_books_list_accessible_for_unauthenticated():
    """Books list endpoint must be available for unauthenticated users."""
    Book.objects.create(
        title="Book1", author="A", cover="HARD", inventory=1, daily_fee=1.0
    )
    client = APIClient()
    url = reverse("book-list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data[0]["title"] == "Book1"
