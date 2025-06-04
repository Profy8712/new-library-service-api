from django.db import models
from borrowings.models import Borrowing


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    borrowing = models.ForeignKey(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    status = models.CharField(
        max_length=7, choices=Status.choices, default=Status.PENDING
    )
    type = models.CharField(
        max_length=7, choices=Type.choices, default=Type.PAYMENT
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=7, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.borrowing} | {self.type} | {self.status} | ${self.money_to_pay}"

