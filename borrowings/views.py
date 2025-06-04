from rest_framework import viewsets, permissions
from .models import Borrowing
from .serializers import BorrowingReadSerializer


class BorrowingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving Borrowings.
    Only authenticated users can view their borrowings.
    Admins see all.
    """
    queryset = Borrowing.objects.select_related("user", "book").all()
    serializer_class = BorrowingReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)

