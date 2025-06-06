from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.services import StripeSessionService

from borrowings.models import Borrowing


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing and creating payments.
    """
    queryset = Payment.objects.select_related("borrowing", "borrowing__user").all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset
        if user.is_staff:
            return qs
        return qs.filter(borrowing__user=user)

    @action(detail=False, methods=["post"], url_path="create")
    def create_payment(self, request):
        borrowing_id = request.data.get("borrowing_id")
        payment_type = request.data.get("type", Payment.Type.PAYMENT)
        try:
            borrowing = Borrowing.objects.get(id=borrowing_id)
        except Borrowing.DoesNotExist:
            return Response({"detail": "Borrowing not found."}, status=404)

        # Здесь простой расчет суммы, можно заменить на свою логику (например, с учетом дней)
        amount = float(borrowing.book.daily_fee)
        session_info = StripeSessionService.create_payment_session(
            borrowing, amount, payment_type
        )
        payment = Payment.objects.create(
            borrowing=borrowing,
            status=Payment.Status.PENDING,
            type=payment_type,
            session_url=session_info["session_url"],
            session_id=session_info["session_id"],
            money_to_pay=amount
        )
        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
