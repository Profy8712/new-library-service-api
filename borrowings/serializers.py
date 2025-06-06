from rest_framework import serializers
from .models import Borrowing
from books.serializers import BookSerializer


class BorrowingReadSerializer(serializers.ModelSerializer):
    """Serializer for read-only Borrowing with nested book info."""
    book = BookSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Borrowing objects."""

    class Meta:
        model = Borrowing
        fields = ("book", "expected_return_date")

    def validate(self, attrs):
        book = attrs.get("book")
        if book.inventory < 1:
            raise serializers.ValidationError("Book is out of stock.")
        return attrs
