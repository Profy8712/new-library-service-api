from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for a Book model."""

    class Meta:
        model = Book
        fields = "__all__"
