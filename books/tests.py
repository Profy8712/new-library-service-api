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

