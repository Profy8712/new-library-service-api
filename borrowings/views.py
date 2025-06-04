from rest_framework import viewsets, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingReadSerializer,
    BorrowingCreateSerializer
)
from borrowings.filters import BorrowingFilter

from notifications.tasks import send_telegram_notification_task


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
        borrowing = serializer.save(user=self.request.user)

        # Telegram notification via Celery
        message = (
            f"📚 New borrowing!\n"
            f"User: {self.request.user.email}\n"
            f"Book: {book.title}\n"
            f"Borrowed at: {borrowing.borrow_date}\n"
            f"Return by: {borrowing.expected_return_date}"
        )
        send_telegram_notification_task.delay(message)

    @action(detail=True, methods=["post"], url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date is not None:
            return Response(
                {"detail": "Borrowing already returned."},
                status=status.HTTP_400_BAD_REQUEST
            )
        from datetime import date
        borrowing.actual_return_date = date.today()
        borrowing.save()
        book = borrowing.book
        book.inventory += 1
        book.save()
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)
