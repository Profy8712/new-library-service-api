from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "borrowing", "status", "type", "money_to_pay", "created_at"
    )
    search_fields = ("borrowing__id", "session_id")
    list_filter = ("status", "type")

