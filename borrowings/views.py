from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Borrowing
from .serializers import BorrowingReadSerializer, BorrowingCreateSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    """
    Borrowing CRUD: read/list for all, create for users.
    """
    queryset = Borrowing.objects.select_related("user", "book").all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        # inventory validation (in addition to serializer)
        if book.inventory < 1:
            raise serializers.ValidationError("Book is out of stock.")
        book.inventory -= 1
        book.save()
        serializer.save(user=self.request.user)
