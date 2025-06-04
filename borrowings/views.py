from django_filters.rest_framework import DjangoFilterBackend

from books import permissions
from .filters import BorrowingFilter
from .models import Borrowing
from .serializers import BorrowingCreateSerializer, BorrowingReadSerializer


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
