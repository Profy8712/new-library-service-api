from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from books import permissions
from borrowings import serializers
from borrowings.filters import BorrowingFilter
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingCreateSerializer, BorrowingReadSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user", "book").all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BorrowingFilter

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset
        user_id = self.request.query_params.get("user")
        if not user.is_staff:
            qs = qs.filter(user=user)
        elif user_id:
            qs = qs.filter(user_id=user_id)
        return qs

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        if book.inventory < 1:
            raise serializers.ValidationError("Book is out of stock.")
        book.inventory -= 1
        book.save()
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date is not None:
            return Response(
                {"detail": "Borrowing already returned."},
                status=status.HTTP_400_BAD_REQUEST
            )
        borrowing.actual_return_date = request.data.get("actual_return_date") or None
        if not borrowing.actual_return_date:
            from datetime import date
            borrowing.actual_return_date = date.today()
        borrowing.save()
        # increment inventory
        book = borrowing.book
        book.inventory += 1
        book.save()
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)
