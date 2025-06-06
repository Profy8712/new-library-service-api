from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""

    borrowing = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id", "borrowing", "status", "type", "session_url",
            "session_id", "money_to_pay", "created_at"
        )
        read_only_fields = fields
