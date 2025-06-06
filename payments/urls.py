from django.urls import path
from .webhooks import stripe_webhook_view
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = router.urls + [
    path("stripe/webhook/", stripe_webhook_view, name="stripe-webhook"),
]
