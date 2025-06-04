from rest_framework import viewsets, permissions
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve payments."""
    queryset = Payment.objects.select_related("borrowing", "borrowing__user").all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset
        if user.is_staff:
            return qs
        return qs.filter(borrowing__user=user)
